package com.dreamteam.hackupc2017.dostuff.Network;


import com.google.gson.GsonBuilder;

import java.io.File;
import java.io.IOException;
import java.util.List;

import io.reactivex.Single;
import okhttp3.Cache;
import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.adapter.rxjava2.RxJava2CallAdapterFactory;
import retrofit2.converter.gson.GsonConverterFactory;

public class NetworkModule {
    private static final String BING_BASE_URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/";
    private static final String WE_GO_BASE_URL = "http://52.17.111.72:5000/";

    private final BingSearchApi searchApi;
    private final WeGoApi weGoApi;

    int cacheSize = 40 * 1024 * 1024; // 40 MB
    public Cache cache;

    static NetworkModule instance;

    public static NetworkModule getInstance(File cacheDir) {
        if (instance == null) {
            instance = new NetworkModule(cacheDir);
        }
        return instance;
    }

    private NetworkModule(File cacheDir) {

        try {
            cache = new Cache(File.createTempFile("cache", "cache"), cacheSize);
        } catch (IOException e) {
            e.printStackTrace();
        }
        OkHttpClient okHttpClient = new OkHttpClient.Builder()
                .cache(cache)
                .build();
        Retrofit bingInstance = new Retrofit.Builder()
                .client(okHttpClient)
                .baseUrl(BING_BASE_URL)
                .addConverterFactory(GsonConverterFactory.create(
                        new GsonBuilder().excludeFieldsWithoutExposeAnnotation().create()))
                .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
                .build();
        searchApi = bingInstance.create(BingSearchApi.class);
        Retrofit weGoInstance = new Retrofit.Builder()
                .client(okHttpClient)
                .baseUrl(WE_GO_BASE_URL)
                .addConverterFactory(GsonConverterFactory.create(
                        new GsonBuilder().excludeFieldsWithoutExposeAnnotation().create()))
                .addCallAdapterFactory(RxJava2CallAdapterFactory.create())
                .build();
        weGoApi = weGoInstance.create(WeGoApi.class);
    }

    public Single<BingResponse> getIcon(String name) {
        return searchApi.getIcon(name, 1);
    }

    public Single<List<Activity>> getActivities() {
        return weGoApi.getActivities();
    }

    public Single<List<Like>> getLikes(long id) {
        return weGoApi.getLikes(id);
    }

    public Single<Object> addLike(long id, long userId, String userName) {
       return weGoApi.addLike(id, userId, "@ig_kholopov", userName).onErrorReturnItem(new Status());
    }

    public Single<Status> removeLike(long id, long userId) {
        return weGoApi.removeLike(id, userId);
    }

    public Single<Object> addActivity(long userId, String userName, String activityName, String description) {
        return weGoApi.addActivity(userId, userName, activityName, activityName, "@ig_kholopov", description);
    }
}
