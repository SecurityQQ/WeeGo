package com.dreamteam.hackupc2017.dostuff;


import android.app.Application;

import com.dreamteam.hackupc2017.dostuff.Network.NetworkModule;


public class App extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        NetworkModule.getInstance(getCacheDir());
    }
}
