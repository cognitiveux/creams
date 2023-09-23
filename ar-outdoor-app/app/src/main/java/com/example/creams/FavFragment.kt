package com.example.creams

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.google.zxing.integration.android.IntentIntegrator

class FavFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_fav, container, false)

        val scanQRButton = view.findViewById<Button>(R.id.scanQRButton)
        scanQRButton.setOnClickListener {
            startQrCodeScanner()
        }

        return view
    }

    private fun startQrCodeScanner() {
        // Initialize the QR code scanner
        val integrator = IntentIntegrator.forSupportFragment(this)
        integrator.setDesiredBarcodeFormats(IntentIntegrator.QR_CODE)
        integrator.setPrompt("Scan a QR code")
        integrator.setBeepEnabled(false)
        integrator.setOrientationLocked(false) // Allow orientation change
        integrator.initiateScan()
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        // Handle QR code scan result
        val result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data)
        if (result != null) {
            val scannedUrl = result.contents
            if (scannedUrl != null && scannedUrl.isNotEmpty()) {
                // Convert scannedUrl to Uri
                val uri = Uri.parse(scannedUrl)

                // Open ArActivity and pass the Uri to it
                val intent = Intent(activity, ArActivity::class.java)
                intent.putExtra("imageUri", uri)
                startActivity(intent)
            } else {
                // Show a toast message when the scannedUrl is empty or null
                Toast.makeText(activity, "Scanned URL is empty or null", Toast.LENGTH_SHORT).show()
            }
        }
    }


}
