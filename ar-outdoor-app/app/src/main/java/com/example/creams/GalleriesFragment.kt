package com.example.creams

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import androidx.fragment.app.Fragment
import coil.load

// TODO: Remove urls when APIs are completed, these are for testing

private const val imgurl = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/1665_Girl_with_a_Pearl_Earring.jpg/800px-1665_Girl_with_a_Pearl_Earring.jpg"
private const val imgurl2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/405px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg"
private const val imgurl3 = "https://maryckhayes.files.wordpress.com/2010/07/cubicle_gothic1.jpg"
private const val imgurl4 = "https://i.ytimg.com/vi/j24uh8cZ3wA/maxresdefault.jpg"

// TODO: Rename parameter arguments, choose names that match
// The fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

/**
 * A simple [Fragment] subclass.
 * Use the [GalleriesFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class GalleriesFragment : Fragment() {
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
        return inflater.inflate(R.layout.fragment_galleries, container, false)
    }

    @SuppressLint("CutPasteId")
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)


        // TODO: Replace View By Id with Recycler View
        val img = view.findViewById<ImageView>(R.id.firstGallery)
        img.load(imgurl)
        val img2 = view.findViewById<ImageView>(R.id.secondGallery)
        img2.load(imgurl2)
        val img3 = view.findViewById<ImageView>(R.id.thirdGallery)
        img3.load(imgurl3)
        val img4 = view.findViewById<ImageView>(R.id.fourthGallery)
        img4.load(imgurl4)


        // TODO: Add all the listeners from the Recycler View
        val image_view_gal = view.findViewById(R.id.firstGallery) as ImageView
        image_view_gal.setOnClickListener {
            activity?.let{
                val intent = Intent(it, MapsActivity::class.java)
                it.startActivity(intent)
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
         * @return A new instance of fragment GalleriesFragment.
         */
        // TODO: Rename and change types and number of parameters
        @JvmStatic
        fun newInstance(param1: String, param2: String) =
            GalleriesFragment().apply {
                arguments = Bundle().apply {
                    putString(ARG_PARAM1, param1)
                    putString(ARG_PARAM2, param2)
                }
            }
    }
}