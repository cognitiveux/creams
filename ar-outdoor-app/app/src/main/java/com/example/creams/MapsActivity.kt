package com.example.creams

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Location
import android.net.Uri
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.example.creams.databinding.ActivityMapsBinding
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.*
import okhttp3.*


@Suppress("DEPRECATION")
class
MapsActivity : AppCompatActivity(), OnMapReadyCallback, GoogleMap.OnMarkerClickListener,
    GoogleMap.OnInfoWindowClickListener {

    private lateinit var mMap: GoogleMap
    private lateinit var binding: ActivityMapsBinding
    private lateinit var lastLocation: Location
    private lateinit var fusedLocationClient: FusedLocationProviderClient

    // HashMap for Images in Markers (Popup Adapter Magics)
    private val images: HashMap<String, Uri> = HashMap<String, Uri>()



    companion object {
        const val LOCATION_REQUEST_CODE = 1
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMapsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        val mapFragment = supportFragmentManager.findFragmentById(R.id.map) as SupportMapFragment
        mapFragment.getMapAsync(this)

        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)

    }

    // Manipulates the map once available.
    // This callback is triggered when the map is ready to be used and is where we can add markers or lines, add listeners or move the camera.

    override fun onMapReady(googleMap: GoogleMap) {
        mMap = googleMap
        mMap.uiSettings.isZoomControlsEnabled = true
        mMap.setOnMarkerClickListener(this)

        // Fetching the data
        val button_id = intent.getIntExtra("button_id",-1)
        val artworklistlat = intent.getSerializableExtra("artworklistlat") as ArrayList<*>
        val artworklistlon = intent.getSerializableExtra("artworklistlon") as ArrayList<*>
        val artworklistname = intent.getStringArrayListExtra("artworklistname")
        val artworklistsrc = intent.getStringArrayListExtra("artworklistsrc")
        val artworklistowneridart = intent.getStringArrayListExtra("artworklistowneridart")

        when (button_id) {
            1 -> {
                // Create the Markers based on PopupAdapter when closest gallery is clicked
                for (i in 0 until artworklistlat.size) {
                    addMarker(mMap, artworklistlat[i] as Double, artworklistlon[i] as Double,
                        artworklistname?.get(i),
                        "by ${artworklistowneridart?.get(i)}", artworklistsrc?.get(i))
                }
                mMap.setInfoWindowAdapter(PopupAdapter(this, layoutInflater, images))
                mMap.setOnInfoWindowClickListener(this)
                setUpMap(button_id, artworklistlat, artworklistlon, artworklistsrc)
            }
            2 -> {
                // Create the Markers based on PopupAdapter when closest artwork is clicked
                for (i in 0 until artworklistlat.size) {
                    addMarker(mMap, artworklistlat[i] as Double, artworklistlon[i] as Double,
                        artworklistname?.get(i),
                        "by ${artworklistowneridart?.get(i)}", artworklistsrc?.get(i))
                }
                mMap.setInfoWindowAdapter(PopupAdapter(this, layoutInflater, images))
                mMap.setOnInfoWindowClickListener(this)
                setUpMap(button_id, artworklistlat, artworklistlon, artworklistsrc)
            }
            else -> {
                // Create the Marker for the clicked artwork
                if (artworklistlat.isNotEmpty() && artworklistlon.isNotEmpty()) {
                    addMarker(
                        mMap, artworklistlat[0] as Double, artworklistlon[0] as Double,
                        artworklistname?.get(0),
                        "by ${artworklistowneridart?.get(0)}", artworklistsrc?.get(0)
                    )
                }
                mMap.setInfoWindowAdapter(PopupAdapter(this, layoutInflater, images))
                mMap.setOnInfoWindowClickListener(this)
                setUpMap(button_id, artworklistlat, artworklistlon, artworklistsrc)
            }
        }
    }







    private fun setUpMap(button_id: Int, latitudes: ArrayList<*>, longitudes: ArrayList<*>, images: ArrayList<String>?) {

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
            != PackageManager.PERMISSION_GRANTED ) {

            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), LOCATION_REQUEST_CODE)
            return
        }
        mMap.isMyLocationEnabled = true
        fusedLocationClient.lastLocation.addOnSuccessListener(this) { location ->

            if (location != null) {
                when (button_id) {
                    0 -> {
                        if (latitudes.isNotEmpty() && longitudes.isNotEmpty()) {
                            val clickedArtworkLat = latitudes[0] as Double
                            val clickedArtworkLon = longitudes[0] as Double
                            val clickedArtworkLatLng = LatLng(clickedArtworkLat, clickedArtworkLon)
                            mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(clickedArtworkLatLng, 18f))
                        }
                    }
                    1 -> {
                        // Closest gallery button clicked
                        lastLocation = location
                        val currentLatLong = LatLng (location.latitude, location.longitude)
                        //placeMarkerOnMap(currentLatLong)
                        mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(currentLatLong, 18f))

                    }
                    2 -> {
                        // Closest artwork button clicked
                        lastLocation = location
                        val currentLatLong = LatLng (location.latitude, location.longitude)
                        //placeMarkerOnMap(currentLatLong)
                        mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(currentLatLong, 18f))

                    }
                }
            }
        }
    }







    private fun placeMarkerOnMap(currentLatLong: LatLng) {
        val markerOptions = MarkerOptions().position(currentLatLong)
        markerOptions.title("$currentLatLong")
        mMap.addMarker(markerOptions)

    }







    override fun onMarkerClick(p0: Marker) = false







    private fun addMarker(map: GoogleMap, lat: Double, lon: Double, title: String?, snippet: String?, image: String?) {
        val marker = map.addMarker(
            MarkerOptions().position(LatLng(lat, lon))
                .title(title)
                .snippet(snippet)
        )
        if (image != null) {
            val imageUri = Uri.parse("https://creams-api.cognitiveux.net/media/$image")
            images[marker!!.id] = imageUri
        }
    }





    override fun onInfoWindowClick(marker: Marker) {
        if (ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_COARSE_LOCATION
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return
        }
        fusedLocationClient.lastLocation.addOnSuccessListener { location ->
            if (location != null) {
                val userLocation = LatLng(location.latitude, location.longitude)
                val markerLocation = marker.position
                val distance = calculateDistance(userLocation, markerLocation)

                val maxDistance = 20 // Specify the maximum allowed distance in meters

                if (distance <= maxDistance) {
                    // User's location is close to the marker's location, start ArActivity
                    Toast.makeText(this, marker.title, Toast.LENGTH_LONG).show()

                    val imageUri = images[marker.id]

                    val intent = Intent(this, ArActivity::class.java).apply {
                        putExtra("latitude", marker.position.latitude)
                        putExtra("longitude", marker.position.longitude)
                        putExtra("imageUri", imageUri)
                    }
                    startActivity(intent)
                } else {
                    Toast.makeText(this, "Marker is too far away.", Toast.LENGTH_LONG).show()
                }
            }
        }
    }

    private fun calculateDistance(location1: LatLng, location2: LatLng): Float {
        val results = FloatArray(1)
        Location.distanceBetween(
            location1.latitude, location1.longitude,
            location2.latitude, location2.longitude,
            results
        )
        return results[0]
    }




    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        // Clear the map's state to prevent crashes when restoring the activity
        outState.clear()
    }






}
