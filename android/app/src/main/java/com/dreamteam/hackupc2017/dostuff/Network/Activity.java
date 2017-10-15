package com.dreamteam.hackupc2017.dostuff.Network;


import android.support.annotation.Nullable;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Activity {
    @SerializedName("author_name")
    @Expose
    public String AuthorName;
    @SerializedName("full_message")
    @Expose
    public String FullMessage;
    @SerializedName("author")
    @Expose
    public Long AuthorId;
    @SerializedName("id")
    @Expose
    public Long Id;
    @SerializedName("title")
    @Expose
    public String Title;
    @SerializedName("author_username")
    @Expose
    @Nullable
    public String AuthorUsername;
}
