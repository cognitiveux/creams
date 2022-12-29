package com.example.creamsdigitizer;

import android.os.AsyncTask;
import android.webkit.CookieManager;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class OkHtttpArtwork_OLD extends AsyncTask {

    OkHttpClient client = new OkHttpClient();

    @Override
    protected String doInBackground(Object [] object) {

        Request.Builder builder = new Request.Builder();


        builder.url((String) object[0]);
        MediaType mediaType = MediaType.parse("text/plain");
        RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
                .addFormDataPart("src","file")
                .addFormDataPart("title","string")
                .build();

        Request request = new Request.Builder()
                .url("http://creams-api.cognitiveux.net/web_app/artworks/create")
                .method("POST", body)
                .build();

        try {
            Response response = client.newCall(request).execute();
            CookieManager cookieManager = CookieManager.getInstance();
            String cookies = cookieManager.getCookie("access_tkn");
            if(cookies != null){
                String[] temp=cookies.split(";");
                for (String ar1 : temp ){
                    if(ar1.contains("access_tkn")){
                        String[] temp1=ar1.split("=");
                        System.out.println(temp1[1]);
                    }
                }
            }

            assert response.body() != null;
            String message = response.body().string();
            System.out.println(message);

            return message;
        }catch (Exception e){
            e.printStackTrace();
        }
        return null;
    }







}