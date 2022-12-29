package com.example.creams

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import kotlinx.android.synthetic.main.fragment_fav.*
import kotlinx.android.synthetic.main.fragment_home.*
import okhttp3.*
import okio.IOException
import org.json.JSONObject


class HomeFragment : Fragment() {



    // Initialization of adapter (Nikos is love)
    val gson: Gson = GsonBuilder().create()
    var outdoorGalleries: OutdoorGalleryModel = gson.fromJson("{\"exhibitions\":[]}",OutdoorGalleryModel::class.java)

    ///////////////////////////////////////
    //var outdoorGalleriesArtworks: OutdoorGalleries = gson.fromJson("{\"artworks\":[]}",OutdoorGalleries::class.java)

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {

        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_home, container, false)

        val recyclerView_Galleries_Home = view?.findViewById(R.id.recyclerView_Galleries_Home) as RecyclerView
        recyclerView_Galleries_Home.layoutManager = GridLayoutManager(context, 1,  RecyclerView.HORIZONTAL,false )
        recyclerView_Galleries_Home.adapter = MainAdapter(outdoorGalleries)


        fetchJson()

        return view
    }

    @SuppressLint("CutPasteId")
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        /* TO DO : Put button stuff in function */

        // Closest Gallery Button
        val dis_closest_gallery_button = view.findViewById(R.id.dis_closest_gallery_button) as Button
        dis_closest_gallery_button.setOnClickListener {
            val button_id = 1
            val artworklistlat = arrayListOf<Double>()
            val artworklistlon = arrayListOf<Double>()
            val artworklistsrc = arrayListOf<String>()
            val artworklistname = arrayListOf<String>()
            var ownername = arrayListOf<String>()
            var artworklistownerid = arrayListOf<String>()
            val artworklistowneridart = arrayListOf<String>()
            val num_exhibitions = outdoorGalleries.exhibitions.size

            activity?.let{
                //fetchJsonButton (button_id)
                //Thread.sleep(2_000)
                val bundle = Bundle()
                val intent = Intent (it, MapsActivity::class.java)

                // Bundle up the exhibition and artwork info
                //bundle.putString("ownername", outdoorGalleries.exhibitions[1].owner_name)

                for (i in 0 until num_exhibitions ) {
                    ownername += outdoorGalleries.exhibitions[i].owner_name
                    artworklistownerid += outdoorGalleries.exhibitions[i].owner /*id of owner in exhibition*/
                    artworklistowneridart += outdoorGalleries.exhibitions[i].artworks.map { it.owner } as ArrayList<String> /*id of owner in artworks*/
                    artworklistname += outdoorGalleries.exhibitions[i].artworks.map { it.name } as ArrayList<String>
                    artworklistlat += outdoorGalleries.exhibitions[i].artworks.map { it.lat } as ArrayList<Double>
                    artworklistlon += outdoorGalleries.exhibitions[i].artworks.map { it.lon } as ArrayList<Double>
                    artworklistsrc += outdoorGalleries.exhibitions[i].artworks.map { it.src } as ArrayList<String>
                }

                bundle.putInt("button_id",  button_id)

                // artworks_size = Number of ALL the artworks
                bundle.putInt("artworks_size", artworklistname.size)
                bundle.putStringArrayList("artworklistname",  artworklistname)
                bundle.putSerializable("artworklistlat", artworklistlat)
                bundle.putSerializable("artworklistlon", artworklistlon)
                bundle.putStringArrayList("artworklistsrc", artworklistsrc)

                // Remove duplicates
                artworklistownerid = artworklistownerid.distinct() as ArrayList<String>
                ownername = ownername.distinct() as ArrayList<String>

                // Create Array List with painters' names
                for (i in 0 until artworklistowneridart.size) {
                    for (j in 0 until artworklistownerid.size) {
                        if (artworklistownerid[j] == artworklistowneridart[i]) {
                            artworklistowneridart[i] = ownername [j]
                        }
                    }
                }
                // Bundle painters' names according to their id
                bundle.putStringArrayList("artworklistowneridart",artworklistowneridart)
                Thread.sleep(1_000)
                // Add bundle to intent and send to intended activity
                intent.putExtras(bundle)
                it.startActivity(intent)
            }
        }



        // Closest Artwork Button
        val dis_closest_artwork_button = view.findViewById(R.id.dis_closest_artwork_button) as Button
        dis_closest_artwork_button.setOnClickListener {
            val button_id = 2
            val artworklistlat = arrayListOf<Double>()
            val artworklistlon = arrayListOf<Double>()
            val artworklistsrc = arrayListOf<String>()
            val artworklistname = arrayListOf<String>()
            var ownername = arrayListOf<String>()
            var artworklistownerid = arrayListOf<String>()
            val artworklistowneridart = arrayListOf<String>()
            val num_exhibitions = outdoorGalleries.exhibitions.size

            activity?.let{
                //fetchJsonButton (button_id)
                //Thread.sleep(2_000)
                val bundle = Bundle()
                val intent = Intent (it, MapsActivity::class.java)

                // Bundle up the exhibition and artwork info
                //bundle.putString("ownername", outdoorGalleries.exhibitions[1].owner_name)

                for (i in 0 until num_exhibitions ) {
                    ownername += outdoorGalleries.exhibitions[i].owner_name
                    artworklistownerid += outdoorGalleries.exhibitions[i].owner /*id of owner in exhibition*/
                    artworklistowneridart += outdoorGalleries.exhibitions[i].artworks.map { it.owner } as ArrayList<String> /*id of owner in artworks*/
                    artworklistname += outdoorGalleries.exhibitions[i].artworks.map { it.name } as ArrayList<String>
                    artworklistlat += outdoorGalleries.exhibitions[i].artworks.map { it.lat } as ArrayList<Double>
                    artworklistlon += outdoorGalleries.exhibitions[i].artworks.map { it.lon } as ArrayList<Double>
                    artworklistsrc += outdoorGalleries.exhibitions[i].artworks.map { it.src } as ArrayList<String>
                }

                bundle.putInt("button_id",  button_id)

                // artworks_size = Number of ALL the artworks
                bundle.putInt("artworks_size", artworklistname.size)
                bundle.putStringArrayList("artworklistname",  artworklistname)
                bundle.putSerializable("artworklistlat", artworklistlat)
                bundle.putSerializable("artworklistlon", artworklistlon)
                bundle.putStringArrayList("artworklistsrc", artworklistsrc)


                // Remove duplicates
                artworklistownerid = artworklistownerid.distinct() as ArrayList<String>
                ownername = ownername.distinct() as ArrayList<String>

                // Create Array List with painters' names
                for (i in 0 until artworklistowneridart.size) {
                    for (j in 0 until artworklistownerid.size) {
                        if (artworklistownerid[j] == artworklistowneridart[i]) {
                            artworklistowneridart[i] = ownername [j]
                        }
                    }
                }
                // Bundle painters' names according to their id
                bundle.putStringArrayList("artworklistowneridart",artworklistowneridart)
                Thread.sleep(1_000)
                // Add bundle to intent and send to intended activity
                intent.putExtras(bundle)
                it.startActivity(intent)
            }
        }

    }



    fun fetchJson() {

        // Val url that doesn't change
        val url = "http://creams-api.cognitiveux.net/web_app/exhibitions/outdoor/all"

        // Construct the request
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

                //val gson = GsonBuilder().create()
                outdoorGalleries = gson.fromJson(resource_obj,OutdoorGalleryModel::class.java)
                activity?.runOnUiThread(Runnable {
                    recyclerView_Galleries_Home.adapter = MainAdapter(outdoorGalleries)
                })
            }
            override fun onFailure(call: Call, e: IOException) {
                println("Failed to execute request")
                e.printStackTrace()
            }
        } )
    }






}