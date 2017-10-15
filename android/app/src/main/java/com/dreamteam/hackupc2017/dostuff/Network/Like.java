package com.dreamteam.hackupc2017.dostuff.Network;


import android.support.annotation.Nullable;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Like {
    @SerializedName("person_name")
    @Expose
    public String PersonName;
    @SerializedName("person")
    @Expose
    public Long PersonId;
    @SerializedName("person_username")
    @Nullable
    @Expose
    public String  PersonUsername;
}
