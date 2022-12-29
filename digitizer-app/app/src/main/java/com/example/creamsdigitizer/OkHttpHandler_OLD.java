package com.example.creamsdigitizer;

import android.os.AsyncTask;
import android.webkit.CookieManager;

import org.json.JSONException;
import org.json.JSONObject;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class OkHttpHandler_OLD extends AsyncTask {

    OkHttpClient client = new OkHttpClient();

    @Override
    protected String doInBackground(Object [] object) {

        Request.Builder builder = new Request.Builder();


        builder.url((String) object[0]);
        MediaType mediaType = MediaType.parse("text/plain");
        RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
                .addFormDataPart("email","creams-asdasdstudent@cognitiveux.de")
                .addFormDataPart("password","Aa12345!")
                .build();

        Request request = new Request.Builder()
                .url("http://creams-api.cognitiveux.net/web_app/account-mgmt/login")
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
                        //System.out.println(temp1[1]);
                    }
                }
            }

            assert response.body() != null;
            String message = response.body().string();

            System.out.println(message);

            try {
               // JSONArray jar = new JSONArray(message);

                JSONObject jsonObject=null;

                jsonObject= new JSONObject(message);

                String access = jsonObject.getString("resource_obj");

                if(!access.equals(null))
                {
                    System.out.println("login successful");
                }

               /* System.out.println("test "+resource);

                if(resource.equals("test User not found"))
                {
                    //incorrect login
                }
                else
                {
                    //correct
                }*/

               // jsonObject= new JSONObject(resource);

               // System.out.println("json object: "+ jsonObject.getString("access"));



              //  jsonObject = jar.getJSONObject(0);
              //  System.out.println(jsonObject.getString("resource_name"));
//                if (jsonObject.getBoolean("resource_name")== true) {

//
//                    JSONObject dataObj= jsonObject.getJSONObject("resource_name");
//                    String jwt= dataObj.getString("access");
//                    System.out.println(jwt);

                    ////RETRIEVE "token" HERE
//                } else {



            } catch (JSONException e) {
                e.printStackTrace();
                System.out.println("login failed");

            }

            return message;
        }catch (Exception e){
            e.printStackTrace();
        }
        return null;
    }
}