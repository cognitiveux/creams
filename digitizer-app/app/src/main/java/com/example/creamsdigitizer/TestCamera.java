package com.example.creamsdigitizer;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.webkit.CookieManager;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.FileProvider;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class TestCamera extends AppCompatActivity {

    private String currentPhotoPath;
    public String url= "http://creams-api.cognitiveux.net/web_app/demo/?format=openapi";

    File imageFile;
    @SuppressLint("MissingInflatedId")
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_test_camera);
        findViewById(R.id.button2).setEnabled(false);

        findViewById(R.id.button).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String filename = "photos";
                File storageDirectory = getExternalFilesDir(Environment.DIRECTORY_PICTURES);

                try {
                    imageFile = File.createTempFile(filename, ".jpg", storageDirectory);
                    currentPhotoPath = imageFile.getAbsolutePath();
                    Uri imageUri  = FileProvider.getUriForFile(TestCamera.this, "com.example.creamsdigitizer.fileprovider", imageFile );


                    Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                    intent.putExtra(MediaStore.EXTRA_OUTPUT, imageUri);
                    startActivityForResult(intent, 1);
                    findViewById(R.id.button).setEnabled(false);
                    findViewById(R.id.button2).setEnabled(true);


                } catch (IOException e) {
                    e.printStackTrace();
                }

            }
        });
        findViewById(R.id.button2).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                UploadButton();
            }

            private void UploadButton() {
                TestCamera.OkHttpArtwork OkHttpArtwork= new OkHttpArtwork();
                OkHttpArtwork.execute(url);
            }
        });
    }

    class OkHttpArtwork extends AsyncTask<String,Void,String> {

        OkHttpClient client = new OkHttpClient();
        int isUpload;

        @Override
        public String doInBackground(String... params) {


            MultipartBody.Part filePart = MultipartBody.Part.createFormData("file", imageFile.getName(), RequestBody.create(MediaType.parse("image/*"), imageFile));

            //Call<MyResponse> call = api.uploadAttachment(filePart);



            Request.Builder builder = new Request.Builder();

            builder.url(params[0]);
            MediaType mediaType = MediaType.parse("multipart");
            RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
                    .addFormDataPart("src",imageFile.getName(), RequestBody.create(MediaType.parse("text/csv"), imageFile) )
                    .addFormDataPart("name","title")
                    .addFormDataPart("year", "2022")
                    .addFormDataPart("height","2")
                    .addFormDataPart("width","5")
                    .addFormDataPart("depth", "1")
                    .addFormDataPart("unit", "2")
                    .addFormDataPart("technique","photo")
                    .addFormDataPart("genre","none")
                    .addFormDataPart("art_type","1234")
                    .build();

            // create the cookie
            // Cookie myCookie = new Cookie("name", "value");
            // set the cookie in the request


            Request request = new Request.Builder()
                    .url("http://creams-api.cognitiveux.net/web_app/artworks/create")
                    .method("POST", body).addHeader("Cookie", "access_tkn = eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc1NTEwMDkzLCJqdGkiOiI2ODgzZTE4NjQ2ODQ0NmZiYWE1NjY2MzQ1MDliNmQxMiIsInVzZXJfaWQiOjcsImlzcyI6IkNyZWFtc0F1dGhlbnRpY2F0aW9uIiwiaWF0IjoxNjcwMzI2MDkzLCJzdWIiOiJjcmVhbXMtc3R1ZGVudEBjb2duaXRpdmV1eC5kZSIsIm5hbWUiOiJTdHVkZW50Iiwic3VybmFtZSI6IkFjY291bnQiLCJvcmdhbml6YXRpb24iOiJDVVgiLCJyb2xlIjoiU1RVREVOVCIsImF1ZCI6WyJDb2duaXRpdmVVWCJdfQ.7UuFyxhf1_QMFjp8UMzriMNOgt3s_tuWw76MMLqledw")
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

                try {

                    JSONObject jsonObject=null;

                    jsonObject= new JSONObject(message);

                    String access = jsonObject.getString("resource_name");

                    if(access != null)
                    {
                        System.out.println("Upload Successful!");
                        isUpload=1;

                    }

                } catch (JSONException e) {
                    e.printStackTrace();
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
                Toast.makeText(TestCamera.this, "Upload Succesfull",Toast.LENGTH_LONG).show();
            }
            else if(isUpload==0)
            {
                System.out.println("Upload failed");
                Toast.makeText(TestCamera.this, "Upload Failed",Toast.LENGTH_LONG).show();

            }

        }
    }
    @Override
    protected  void onActivityResult(int requestCode, int resultCode, Intent data) {

        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == 1 && resultCode == RESULT_OK){
            Bitmap bitmap = BitmapFactory.decodeFile(currentPhotoPath);
            ImageView imageView = findViewById(R.id.imageView);
            imageView.setImageBitmap(bitmap);


        }
        byte[] encodedImage = new byte[0];
        byte[] decodedString = Base64.decode(encodedImage, Base64.DEFAULT);
        Bitmap bitmap = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);

        System.out.println("encoded image: " + Arrays.toString(encodedImage));
        System.out.println("decoded string: "+ Arrays.toString(decodedString));
        System.out.println("bitmap: "+bitmap);

    }
}
