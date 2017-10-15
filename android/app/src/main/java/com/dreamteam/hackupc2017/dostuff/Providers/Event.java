package com.dreamteam.hackupc2017.dostuff.Providers;


import com.dreamteam.hackupc2017.dostuff.Network.Activity;
import com.dreamteam.hackupc2017.dostuff.Network.Like;

import java.util.ArrayList;
import java.util.List;

public class Event {
    public long Id;
    public String Title;
    public List<Like> Likes;

    public Event(long id, String title) {
        Id = id;
        Title = title;
        Likes = new ArrayList<>();
    }

    public Event(Activity activity, List<Like> likes) {
        Id = activity.Id;
        Title = activity.Title;
        Likes = likes;
    }
}
