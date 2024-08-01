import React, { useState, useEffect, useCallback } from 'react'; // Importera useCallback
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const { id } = useParams();
  
  const dealer_url = `/djangoapp/get_dealer/${id}`;
  const reviews_url = `/djangoapp/get_dealer_reviews/${id}`;
  const post_review_url = `/postreview/${id}`;

  // Använd useCallback för att memoize funktionerna
  const get_dealer = useCallback(async () => {
    try {
      const res = await fetch(dealer_url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.status === 200 && retobj.dealer) {
        setDealer(retobj.dealer);
      }
    } catch (error) {
      console.error("Error fetching dealer:", error);
    }
  }, [dealer_url]);

  const get_reviews = useCallback(async () => {
    try {
      const res = await fetch(reviews_url, { method: "GET" });
      const retobj = await res.json();
      if (retobj.status === 200) {
        if (retobj.reviews.length > 0) {
          setReviews(retobj.reviews);
        } else {
          setUnreviewed(true);
        }
      }
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  }, [reviews_url]);

  const senti_icon = (sentiment) => {
    switch (sentiment) {
      case "positive":
        return positive_icon;
      case "negative":
        return negative_icon;
      default:
        return neutral_icon;
    }
  };

  useEffect(() => {
    get_dealer();
    get_reviews();
  }, [id, get_dealer, get_reviews]); // Lägg till get_dealer och get_reviews som beroenden

  const isLoggedIn = sessionStorage.getItem("username") !== null;

  return (
    <div style={{ margin: "20px" }}>
      <Header />
      <div style={{ marginTop: "10px" }}>
        <h1 style={{ color: "grey" }}>
          {dealer.full_name}
          {isLoggedIn && (
            <a href={post_review_url}>
              <img src={review_icon} style={{ width: '10%', marginLeft: '10px', marginTop: '10px' }} alt='Post Review' />
            </a>
          )}
        </h1>
        <h4 style={{ color: "grey" }}>
          {dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}
        </h4>
      </div>
      <div className="reviews_panel">
        {reviews.length === 0 && !unreviewed ? (
          <span>Loading Reviews....</span>
        ) : unreviewed ? (
          <div>No reviews yet!</div>
        ) : (
          reviews.map(review => (
            <div className='review_panel' key={review.id}>
              <img src={senti_icon(review.sentiment)} className="emotion_icon" alt='Sentiment' />
              <div className='review'>{review.review}</div>
              <div className="reviewer">
                {review.name} {review.car_make} {review.car_model} {review.car_year}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dealer;
