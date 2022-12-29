package com.example.creams

import android.annotation.SuppressLint
import android.content.Context
import android.net.Uri
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import com.google.android.gms.maps.GoogleMap.InfoWindowAdapter
import com.google.android.gms.maps.model.Marker
import com.squareup.picasso.Callback
import com.squareup.picasso.Picasso
import java.lang.Exception


internal class PopupAdapter(ctxt: Context, inflater: LayoutInflater?, images: HashMap<String, Uri>?) : InfoWindowAdapter {
    private var popup: View? = null
    private var inflater: LayoutInflater? = null
    private var images: HashMap<String, Uri>? = null
    private var ctxt: Context? = null
    private var iconWidth = -1
    private var iconHeight = -1
    private var lastMarker: Marker? = null




    init {
        this.ctxt = ctxt
        this.inflater = inflater
        this.images = images
        iconWidth = ctxt.resources.getDimensionPixelSize(R.dimen.icon_width)
        iconHeight = ctxt.resources.getDimensionPixelSize(R.dimen.icon_height)
    }

    override fun getInfoWindow(marker: Marker): View? {
        return null
    }




    @SuppressLint("InflateParams")
    override fun getInfoContents(marker: Marker): View? {
        if (popup == null) {
            popup = inflater!!.inflate(R.layout.popup, null)
        }
        if (lastMarker == null
            || lastMarker!!.id != marker.id
        ) {
            lastMarker = marker
            var tv = popup!!.findViewById<View>(R.id.title) as TextView
            tv.text = marker.title
            tv = popup!!.findViewById<View>(R.id.snippet) as TextView
            tv.text = marker.snippet
            val image = images!![marker.id]
            val icon = popup!!.findViewById<View>(R.id.icon) as ImageView


            if (image == null) {
                icon.visibility = View.GONE
            } else {
                icon.visibility = View.VISIBLE
                Picasso.get().load(image).resize(iconWidth, iconHeight)
                    .centerCrop().noFade()
                    .placeholder(R.drawable.rounded_button)
                    .into(icon, MarkerCallback(marker))
            }
        }
        return popup
    }



    internal class MarkerCallback(marker: Marker?) : Callback {
        var marker: Marker? = null
        init {
            this.marker = marker
        }

        fun onError() {
            Log.e(javaClass.simpleName, "Error loading thumbnail!")
        }

        override fun onSuccess() {
            if (marker != null && marker!!.isInfoWindowShown) {
                marker!!.showInfoWindow()
            }
        }

        override fun onError(e: Exception?) {
            println("error loading?")
        }
    }
}