package com.example.creams

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import kotlinx.android.synthetic.main.fragment_fav.*
import okhttp3.*
import okio.IOException
import org.json.JSONObject



class FavFragment : Fragment() {

    val gson: Gson = GsonBuilder().create()
    var outdoorGalleries: OutdoorGalleryModel = gson.fromJson("{\"exhibitions\":[]}",OutdoorGalleryModel::class.java)

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_fav, container, false)

        // TODO: Change Favourite's Recycler View
        val recyclerView_Galleries = view?.findViewById(R.id.recyclerView_Galleries) as RecyclerView

        recyclerView_Galleries.layoutManager = GridLayoutManager(context, 1)
        recyclerView_Galleries.adapter = MainAdapter(outdoorGalleries)

        fetchJson()

        return view
    }

    @SuppressLint("SetTextI18n")

    //ALWAYS FINDVIEWBYID IN ONVIEWCREATED

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // TODO: Add all the listeners from the Recycler View
//        val image_view_gal = view.findViewById(R.id.firstGallery) as ImageView
//        image_view_gal.setOnClickListener {
//            activity?.let{
//                val intent = Intent(it, MapsActivity::class.java)
//                it.startActivity(intent)
//            }
//        }
    }

    fun fetchJson() {

        // Val url that doesn't change
        val url = "http://creams-api.cognitiveux.net/web_app/exhibitions/outdoor/all"

        // construct the request
        val request = Request.Builder().url(url).build()
        val client = OkHttpClient()

        // Call the request (execute outside the main thread... enqueued first)
        // Enqueue runs all the request on the background, need to call run on ui to bring in the front
        client.newCall(request).enqueue(object: Callback {
            @SuppressLint("NotifyDataSetChanged")
            override fun onResponse(call: Call, response: Response) {
                val body = response.body?.string()
                val json = JSONObject(body)
                val resource_obj = json.getJSONObject("resource_obj").toString()

                outdoorGalleries = gson.fromJson(resource_obj,OutdoorGalleryModel::class.java)

                activity?.runOnUiThread(Runnable {
                    recyclerView_Galleries.adapter = MainAdapter(outdoorGalleries)
                })
            }
            override fun onFailure(call: Call, e: IOException) {
                println("Failed to execute request")
            }
        })
    }

}
