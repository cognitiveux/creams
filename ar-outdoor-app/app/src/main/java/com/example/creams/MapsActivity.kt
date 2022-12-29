package com.example.creams

import android.Manifest
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

    // HashMap for Images in Markers (Popup Adapter Magics
    private val images: HashMap<String, Uri> = HashMap<String, Uri>()

    companion object {
        const val LOCATION_REQUEST_CODE = 1
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMapsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        val mapFragment = supportFragmentManager
            .findFragmentById(R.id.map) as SupportMapFragment
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

        // Only when recyclerview is clicked:
        val gal_id = intent.getIntExtra("gal_id", -1 )

        val artworks_size = intent.getIntExtra("artworks_size", -1)
        val artworklistname = intent.getStringArrayListExtra("artworklistname")
        val artworklistlat = intent.getSerializableExtra("artworklistlat") as ArrayList<*>
        val artworklistlon = intent.getSerializableExtra("artworklistlon") as ArrayList<*>
        val artworklistsrc = intent.getStringArrayListExtra("artworklistsrc")
        val artworklistowneridart = intent.getStringArrayListExtra("artworklistowneridart")
        val ownername_from_recyclerview = intent.getStringExtra("ownername_from_recyclerview")





        when (button_id) {
            1 -> {
                // Create the Markers based on PopupAdapter when closest gallery is clicked
                for (i in 0 until artworks_size) {
                    addMarker(mMap, artworklistlat[i] as Double, artworklistlon[i] as Double,
                        artworklistname?.get(i),
                        "by ${artworklistowneridart?.get(i)}", artworklistsrc?.get(i))
                }
                mMap.setInfoWindowAdapter(PopupAdapter(this, layoutInflater, images))
                mMap.setOnInfoWindowClickListener(this)
                setUpMap(button_id, artworklistlat, artworklistlon)
            }
            2 -> {

                // Create the Markers based on PopupAdapter when closest artwork is clicked
                for (i in 0 until artworks_size) {
                    addMarker(mMap, artworklistlat[i] as Double, artworklistlon[i] as Double,
                        artworklistname?.get(i),
                        "by ${artworklistowneridart?.get(i)}", artworklistsrc?.get(i))
                }

                mMap.setInfoWindowAdapter(PopupAdapter(this, layoutInflater, images))
                mMap.setOnInfoWindowClickListener(this)
                setUpMap(button_id, artworklistlat, artworklistlon)
            }
            else -> {
                // Create the Markers based on PopupAdapter when a gallery is clicked
                for (i in 0 until gal_id) {
                    addMarker(mMap, artworklistlat[i] as Double, artworklistlon[i] as Double,  artworklistname?.get(i),
                        "by $ownername_from_recyclerview", artworklistsrc?.get(i))
                }
                mMap.setInfoWindowAdapter(PopupAdapter(this, layoutInflater, images))
                mMap.setOnInfoWindowClickListener(this)
                setUpMap(button_id, artworklistlat, artworklistlon)
            }
        }

    }


    private fun setUpMap(button_id: Int, latitudes: ArrayList<*>, longitudes: ArrayList<*>) {

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
            != PackageManager.PERMISSION_GRANTED ) {

            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), LOCATION_REQUEST_CODE)
            return
        }
        mMap.isMyLocationEnabled = true
        fusedLocationClient.lastLocation.addOnSuccessListener(this) { location ->

            if (location != null) {
                if (button_id == 0) {
                    lastLocation = location
                    val currentLatLong = LatLng (location.latitude, location.longitude)
                    //placeMarkerOnMap(currentLatLong)
                    mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(currentLatLong, 18f))
                 }
                else if (button_id == 1 ) {

                    lastLocation = location
                    val currentLatLong = LatLng (location.latitude, location.longitude)
                    //placeMarkerOnMap(currentLatLong)
                    mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(currentLatLong, 18f))

                }
                else if (button_id == 2 ) {

                    lastLocation = location
                    val currentLatLong = LatLng (location.latitude, location.longitude)
                    //placeMarkerOnMap(currentLatLong)
                    mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(currentLatLong, 18f))

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
            images[marker!!.id] = Uri.parse("http://creams-api.cognitiveux.net/media/" + image)
        }
    }

    // Small toast showing the title of the artwork on info window click
    override fun onInfoWindowClick(marker: Marker) {
        Toast.makeText(this, marker.title, Toast.LENGTH_LONG).show()
    }









}
