package com.example.creams

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.os.Parcel
import android.os.Parcelable
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.galleries_row.view.*



private val image_url = "http://creams-api.cognitiveux.net/media/"

class ButtonAdapter(val outdoorGalleries: OutdoorGalleryModel) {

//    init {
//
//    }

//    // Number of exhibitions
//    override fun getItemCount(): Int {
//        return outdoorGalleries.exhibitions.count()
//    }
//
//    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CustomViewHolder {
//        val layoutInflater = LayoutInflater.from(parent.context)
//        val cellForRow = layoutInflater.inflate(R.layout.galleries_row,parent,false)
//        return CustomViewHolder(cellForRow)
//    }
//
//    @SuppressLint("SetTextI18n")
//    override fun onBindViewHolder(holder: CustomViewHolder, position: Int) {
//        val exhibition = outdoorGalleries.exhibitions.get(position)
//        // Titles of Exhibitions in the Recycler View
//        holder.itemView.GalleryIconText.text = exhibition.title
//
//        // Titles of Exhibitions in the Recycler View
//        val by_string = "by \n" + exhibition.owner_name
//        holder.itemView.GalleryOwnerText.text = by_string
//
//        // Thumbnails of Exhibitions in the Recycler View
//        val thumbnailImageUrl = image_url + exhibition.thumbnail
//        Picasso.get().load(thumbnailImageUrl).into(holder.view.GalleryIcon)
//
//        // Refresh with scroll the passing data!!!
//        holder.outdoorGallery = exhibition
//    }
//
//    override fun writeToParcel(parcel: Parcel, flags: Int) {
//
//    }
//
//    override fun describeContents(): Int {
//        return 0
//    }
//
//    companion object CREATOR : Parcelable.Creator<ButtonAdapter> {
//        override fun createFromParcel(parcel: Parcel): ButtonAdapter {
//            return ButtonAdapter(parcel)
//        }
//
//        override fun newArray(size: Int): Array<ButtonAdapter?> {
//            return arrayOfNulls(size)
//        }
//    }
//}
//
//class CustomHolder(val view: View, var outdoorGallery: OutdoorGalleries? = null): RecyclerView.ViewHolder(view) {
//
//    init {
//
//        view.setOnClickListener {
//            val intent = Intent(view.context, MapsActivity::class.java)
//            val bundle = Bundle()
//
//            // Bundle up the exhibition and artwork info
//            //bundle.putString("title", outdoorGallery?.title)
//            bundle.putString("ownername", outdoorGallery?.owner_name)
//            //bundle.putInt("gal_id", outdoorGallery!!.id)
//            bundle.putInt("gal_size", outdoorGallery!!.artworks.size)
//
//            val button_id = 0
//            val artworklistname: ArrayList<String> = outdoorGallery!!.artworks.map { it.name } as ArrayList<String>
//            val artworklistlat: ArrayList<Double> = outdoorGallery!!.artworks.map { it.lat } as ArrayList<Double>
//            val artworklistlon: ArrayList<Double> = outdoorGallery!!.artworks.map { it.lon } as ArrayList<Double>
//            val artworklistsrc: ArrayList<String> = outdoorGallery!!.artworks.map { it.src } as ArrayList<String>
//
//            bundle.putInt("button_id",  button_id)
//            bundle.putStringArrayList("artworklistname",  artworklistname)
//            bundle.putSerializable("artworklistlat", artworklistlat)
//            bundle.putSerializable("artworklistlon", artworklistlon)
//            bundle.putStringArrayList("artworklistsrc",  artworklistsrc)
//
//            // Add bundle to intent and send to intended activity
//            intent.putExtras(bundle)
//            view.context.startActivity(intent)
//            }
//        }

}
