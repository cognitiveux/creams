package com.example.creamsdigitizer;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.webkit.CookieManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class DisplayActivity extends AppCompatActivity {

    ImageView image;
    Button b;
    EditText title;

    OkHttpClient client = new OkHttpClient();
    public String url= "http://creams-api.cognitiveux.net/web_app/demo/?format=openapi";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display);

        title = findViewById(R.id.title);
        image = findViewById(R.id.displayImage);
        b = findViewById(R.id.button);
//        byte[] byteArray = getIntent().getByteArrayExtra("image");
//        Bitmap bmp = BitmapFactory.decodeByteArray(byteArray, 0, byteArray.length);
//
//        String encodedImage = Base64.encodeToString(byteArray, Base64.DEFAULT);
        Bundle extras = getIntent().getExtras();
        byte[] byteArray = extras.getByteArray("picture");

        Bitmap bmp = BitmapFactory.decodeByteArray(byteArray, 0, byteArray.length);
        ImageView image = (ImageView) findViewById(R.id.displayImage);

        image.setImageBitmap(bmp);

        b.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                UploadButton();




            }
        });



    }

    private void UploadButton() {
        OkHttpArtwork OkHttpArtwork= new OkHttpArtwork();
        OkHttpArtwork.execute(url);



    }
    class OkHttpArtwork extends AsyncTask<String,Void,String> {

        OkHttpClient client = new OkHttpClient();
        int isUpload;

        @Override
        protected String doInBackground(String... params) {

            Request.Builder builder = new Request.Builder();

            builder.url(params[0]);
            MediaType mediaType = MediaType.parse("text/plain");
            RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
                    .addFormDataPart("src","enccodeImage")
                    .addFormDataPart("name",title.getText().toString())
                    .addFormDataPart("year", "2022")
                    .addFormDataPart("height","2.50")
                    .addFormDataPart("width","5")
                    .addFormDataPart("depth", "1")
                    .addFormDataPart("unit", "test")
                    .addFormDataPart("technique","photo")
                    .addFormDataPart("genre","none")
                    .addFormDataPart("art_type","painting")
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

                    String access = jsonObject.getString("resource_name");

                    if(!access.equals(null))
                    {
                        System.out.println("login successful");
                        isUpload=1;

                    }


                } catch (JSONException e) {
                    e.printStackTrace();
                    //System.out.println("login failed");
                    isUpload=0;

                }

                return message;
            }catch (Exception e){
                e.printStackTrace();
            }
            return null;
        }

        @Override
        protected void onPreExecute() {

        }

        @Override
        protected void onPostExecute(String result)
        {

            if(isUpload==1)
            {

                System.out.println("Upload success");
            }
            else if(isUpload==0)
            {
                System.out.println("Upload failed");

            }

        }
}


}