package com.example.creams

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import okhttp3.Call
import okhttp3.Callback
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okio.IOException
import org.json.JSONObject

class GalleriesFragment : Fragment() {

    private lateinit var recyclerViewArtworks: RecyclerView
    private lateinit var mainAdapter: MainAdapter
    private val gson: Gson = GsonBuilder().create()

    private val imageUriBase = "https://creams-api.cognitiveux.net/media/"
    private var outdoorGalleries: OutdoorGalleryModel? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_galleries, container, false)
        recyclerViewArtworks = view.findViewById(R.id.recyclerView_Galleries)
        recyclerViewArtworks.layoutManager = GridLayoutManager(context, 2) // Set the number of columns here
        mainAdapter = MainAdapter(OutdoorGalleryModel(emptyList()))
        recyclerViewArtworks.adapter = mainAdapter
        fetchJson()

        // Set a click listener for the items in the adapter
        recyclerViewArtworks.addOnItemClickListener(object : OnItemClickListener {
            // In the GalleriesFragment where you handle item click:
            // In the GalleriesFragment where you handle item click:
            override fun onItemClicked(position: Int) {
                val exhibition = outdoorGalleries?.exhibitions?.get(position)
                if (exhibition != null) {
                    val imageUriString = imageUriBase + exhibition.thumbnail
                    if (imageUriString.isNotEmpty()) {
                        val imageUri = Uri.parse(imageUriString) // Convert the String to Uri
                        openArActivity(imageUri)
                    } else {
                        Toast.makeText(context, "Image URL is empty.", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    Toast.makeText(context, "Exhibition not found.", Toast.LENGTH_SHORT).show()
                }
            }

        })

        return view
    }

    private fun RecyclerView.addOnItemClickListener(onItemClickListener: OnItemClickListener) {
        this.addOnChildAttachStateChangeListener(object : RecyclerView.OnChildAttachStateChangeListener {
            override fun onChildViewAttachedToWindow(view: View) {
                view.setOnClickListener {
                    val position = getChildAdapterPosition(view)
                    if (position != RecyclerView.NO_POSITION) {
                        onItemClickListener.onItemClicked(position)
                    }
                }
            }

            override fun onChildViewDetachedFromWindow(view: View) {
                view.setOnClickListener(null)
            }
        })
    }

    private fun fetchJson() {
        val url = "https://creams-api.cognitiveux.net/web_app/exhibitions/outdoor/all"
        val request = Request.Builder().url(url).build()
        val client = OkHttpClient()

        client.newCall(request).enqueue(object : Callback {
            override fun onResponse(call: Call, response: Response) {
                val body = response.body?.string()
                val json = JSONObject(body)
                val resourceObj = json.getJSONObject("resource_obj").toString()

                outdoorGalleries = gson.fromJson(resourceObj, OutdoorGalleryModel::class.java)

                activity?.runOnUiThread {
                    mainAdapter.outdoorGalleries = outdoorGalleries ?: OutdoorGalleryModel(emptyList())
                    mainAdapter.notifyDataSetChanged()
                }
            }

            override fun onFailure(call: Call, e: IOException) {
                println("Failed to execute request")
            }
        })
    }

    private fun openArActivity(imageUri: Uri) {
        val intent = Intent(activity, ArActivity::class.java)
        intent.putExtra("imageUri", imageUri)
        startActivity(intent)
    }

    // Click listener interface for RecyclerView item clicks
    interface OnItemClickListener {
        fun onItemClicked(position: Int)
    }
}
