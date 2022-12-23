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
class MapsActivity : AppCompatActivity(), OnMapReadyCallback, GoogleMap.OnMarkerClickListener,
    GoogleMap.OnInfoWindowClickListener {

    private lateinit var mMap: GoogleMap
    private lateinit var binding: ActivityMapsBinding
    private lateinit var lastLocation: Location
    private lateinit var fusedLocationClient: FusedLocationProviderClient

    // New addition for image display through Popup adapter
    private val images: HashMap<String, Uri> = HashMap<String, Uri>()

    companion object {
        private const val LOCATION_REQUEST_CODE = 1
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
        //val title = intent.getStringExtra("title" )
        val ownername = intent.getStringExtra("ownername" )
        //val gal_id = intent.getIntExtra("gal_id", -1 )
        val gal_size = intent.getIntExtra("gal_size", -1)
        val artworklistname = intent.getStringArrayListExtra("artworklistname")
        val artworklistlat = intent.getSerializableExtra("artworklistlat") as ArrayList<*>
        val artworklistlon = intent.getSerializableExtra("artworklistlon") as ArrayList<*>
        val artworklistsrc = intent.getStringArrayListExtra("artworklistsrc")


        for (i in 0 until gal_size) {
            addMarker(mMap, artworklistlat[i] as Double, artworklistlon[i] as Double,  artworklistname?.get(i),
                "by $ownername", artworklistsrc?.get(i))
        }

        mMap.setInfoWindowAdapter(PopupAdapter(this, layoutInflater, images))
        mMap.setOnInfoWindowClickListener(this)
        setUpMap()
    }

    private fun setUpMap() {

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
            != PackageManager.PERMISSION_GRANTED ) {

            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), LOCATION_REQUEST_CODE)
            return
        }
        mMap.isMyLocationEnabled = true
        fusedLocationClient.lastLocation.addOnSuccessListener(this) { location ->

            if (location != null) {
                lastLocation = location
                val currentLatLong = LatLng (location.latitude, location.longitude)
                // If wanted, add special marker on maps for user's position
                //placeMarkerOnMap(currentLatLong)
                mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(currentLatLong, 18f))
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
            images[marker!!.id] = Uri.parse("http://creams-api.cognitiveux.net/media/$image")
        }
    }

    override fun onInfoWindowClick(marker: Marker) {
        Toast.makeText(this, marker.title, Toast.LENGTH_LONG).show()
    }









}
