package com.dreamteam.hackupc2017.dostuff.Network;


import java.util.List;

import io.reactivex.Single;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface WeGoApi {
    @GET("get_activities")
    Single<List<Activity>> getActivities();

    @GET("get_likes?")
    Single<List<Like>> getLikes(@Query("activity_id") long id);

    @GET("add_like?")
    Single<Object> addLike(@Query("activity_id") long id,
                           @Query("user_id") long userId,
                           @Query("user_username") String username,
                           @Query("user_name") String userName);

    @GET("remove_like?")
    Single<Status> removeLike(@Query("activity_id") long id,
                           @Query("user_id") long userId);
    @GET("add_activity?")
    Single<Object> addActivity(@Query("user_id") long userId,
                               @Query("user_name") String userName,
                               @Query("activity_name") String activityName,
                               @Query("title") String title,
                               @Query("user_username") String username,
                               @Query("description") String description);
}

