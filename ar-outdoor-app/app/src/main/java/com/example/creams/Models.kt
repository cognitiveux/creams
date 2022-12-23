package com.example.creams

class OutdoorGalleryModel(val exhibitions: List<OutdoorGalleries>)
class OutdoorGalleries (val title: String, val owner_name: String, val thumbnail: String, val artworks: List<OutdoorGalleryArtworks>, val id: Int)
class OutdoorGalleryArtworks(val lat: Double, val lon: Double, val src: String, val name: String)
