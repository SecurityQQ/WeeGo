package com.dreamteam.hackupc2017.dostuff.Network;


import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class BingResponse {
    @SerializedName("value")
    @Expose
    public List<Image> images;
}
