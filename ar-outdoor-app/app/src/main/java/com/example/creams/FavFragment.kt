package com.example.creams

import android.annotation.SuppressLint
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import androidx.fragment.app.Fragment
import okhttp3.*
import java.io.IOException

// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

// TODO: This is a testing click, still needing APIs!
private const val imgurl = "http://creams-api.cognitiveux.net/web_app/artworks/details?artwork-id=2"


/**
 * A simple [Fragment] subclass.
 * Use the [FavFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class FavFragment : Fragment() {
    // TODO: Rename and change types of parameters
    private var param1: String? = null
    private var param2: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {
            param1 = it.getString(ARG_PARAM1)
            param2 = it.getString(ARG_PARAM2)
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_fav, container, false)
    }


    @SuppressLint("SetTextI18n")
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val urlButton = view.findViewById(R.id.urlButton) as Button
        val urlDump = view.findViewById(R.id.urlDump) as TextView

        urlButton.setOnClickListener {

            val URL: String = imgurl
            if (URL.isNotEmpty()) {
                // Creating HTTP Client
                val galleryImageFetch = OkHttpClient()
                // Building the request
                val request = Request.Builder()
                    .url(URL)
                    .build()
                // Enqueue the request and handle the call backs
                galleryImageFetch.newCall(request).enqueue(object : Callback {
                    override fun onFailure(call: Call, e: IOException) {
                        e.printStackTrace();
                    }

                    override fun onResponse(call: Call, response: Response) {
                        Log.i(
                            "Response",
                            "Received response from server"
                        ); //information log for debugging
                        response.use {
                            if (!response.isSuccessful) {
                                Log.e("HTTP Error", "Something didn't load or wasn't successful");
                            } else {
                                // Fetch the body of the response
                                val body =
                                    response.body?.string() // Fetch the body as a separate thread,  can cause issues!
                                urlDump.text =
                                    body // print the body to the textview on the screen
                            }
                        }
                    }
                })
            } else {
                urlDump.text = "URL was empty"
            }
        }

    }

    companion object {
        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment FavFragment.
         */
        // TODO: Rename and change types and number of parameters
        @JvmStatic
        fun newInstance(param1: String, param2: String) =
            FavFragment().apply {
                arguments = Bundle().apply {
                    putString(ARG_PARAM1, param1)
                    putString(ARG_PARAM2, param2)
                }
            }
    }
}