package com.dreamteam.hackupc2017.dostuff.Network;

import io.reactivex.Single;
import retrofit2.http.GET;
import retrofit2.http.Headers;
import retrofit2.http.Query;

public interface BingSearchApi {
    @Headers("Ocp-Apim-Subscription-Key: 4a21d63d0fac4de5bd8ba0a1b1b5569c")
    @GET("search?")
    Single<BingResponse> getIcon(@Query("q") String query,
                          @Query("count") int count);
}
