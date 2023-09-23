package com.example.creams

import android.graphics.Bitmap
import android.graphics.drawable.Drawable
import android.net.Uri
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.google.ar.core.ArCoreApk
import com.google.ar.core.Config
import com.google.ar.core.Session
import com.google.ar.sceneform.AnchorNode
import com.google.ar.sceneform.Node
import com.google.ar.sceneform.math.Vector3
import com.google.ar.sceneform.rendering.MaterialFactory
import com.google.ar.sceneform.rendering.ModelRenderable
import com.google.ar.sceneform.rendering.ShapeFactory
import com.google.ar.sceneform.rendering.Texture
import com.google.ar.sceneform.ux.ArFragment
import com.squareup.picasso.Picasso
import com.squareup.picasso.Target
import java.util.concurrent.CompletableFuture

class ArActivity : AppCompatActivity() {

    private lateinit var arFragment: ArFragment
    private var arSession: Session? = null
    private var imageUri: Uri? = null
    private var isAugmented: Boolean = false // Flag to track if an augmentation has been placed


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_ar)

        arFragment = supportFragmentManager.findFragmentById(R.id.arFragment) as ArFragment

        // Check if ARCore is installed and up to date
        if (ArCoreApk.getInstance().checkAvailability(this) == ArCoreApk.Availability.UNSUPPORTED_DEVICE_NOT_CAPABLE) {
            // ARCore is not supported on this device, handle accordingly
            return
        }

        // Request ARCore installation if not already installed
        if (ArCoreApk.getInstance().requestInstall(this, true) == ArCoreApk.InstallStatus.INSTALL_REQUESTED) {
            // ARCore installation has been requested, pause the activity until installation is complete
            return
        }

        // Get the image URI from the intent
        imageUri = intent.getParcelableExtra("imageUri")
        println("aractivity received:")
        println(imageUri)

        // Create AR session
        arSession = Session(this)
        val config = Config(arSession)
        config.updateMode = Config.UpdateMode.LATEST_CAMERA_IMAGE
        arSession?.configure(config)

        arFragment.setOnTapArPlaneListener { hitResult, _, _ ->
            if (!isAugmented) { // Check if an augmentation has already been placed
                // Create an anchor at the hit location
                val anchor = hitResult.createAnchor()
                val anchorNode = AnchorNode(anchor)
                anchorNode.setParent(arFragment.arSceneView.scene)

                // Create the image renderable
                createImageRenderable { renderable ->
                    if (renderable != null) {
                        // Create a node and attach the renderable to it
                        val node = Node()
                        node.renderable = renderable
                        node.setParent(anchorNode)

                        arFragment.arSceneView.scene.addChild(anchorNode)

                        isAugmented = true // Set the flag to indicate an augmentation has been placed
                    } else {
                        // Handle error when creating the renderable
                        // Show a default renderable or display an error message
                    }
                }
            }
        }
    }


    private fun createImageRenderable(callback: (ModelRenderable?) -> Unit) {
        // Use Picasso to load the image from the URL and convert it to a Bitmap
        Picasso.get()
            .load(imageUri)
            .into(object : Target {
                override fun onBitmapLoaded(bitmap: Bitmap?, from: Picasso.LoadedFrom?) {
                    if (bitmap != null) {
                        // Create a texture from the loaded bitmap
                        val texture = CompletableFuture<Texture>()
                        Texture.builder()
                            .setSource(bitmap)
                            .build()
                            .thenAccept { texture.complete(it) }

                        // Create a Material using the texture
                        texture.thenAccept { tex ->
                            MaterialFactory.makeOpaqueWithTexture(this@ArActivity, tex)
                                .thenAccept { material ->
                                    val width = 0.7f // Adjust the width of the cube (smaller value makes it thinner)
                                    val height = 0.7f // Adjust the height of the cube
                                    val depth = 0.01f // Adjust the depth of the cube (smaller value makes it thinner)

                                    // Create the ModelRenderable using a cube shape and the Material
                                    val renderable = ShapeFactory.makeCube(
                                        Vector3(width, height, depth),
                                        Vector3.zero(),
                                        material
                                    )
                                    callback(renderable)
                                }
                                .exceptionally { throwable ->
                                    // Handle error when creating the material
                                    // Show a default renderable or display an error message
                                    callback(null)
                                    null
                                }
                        }
                    } else {
                        // Handle error when loading the image
                        // Show a default renderable or display an error message
                        callback(null)
                    }
                }

                override fun onBitmapFailed(e: Exception?, errorDrawable: Drawable?) {
                    // Handle error when loading the image
                    // Show a default renderable or display an error message
                    callback(null)
                }

                override fun onPrepareLoad(placeHolderDrawable: Drawable?) {
                    // Optional: Handle image loading preparation
                }
            })
    }




}
