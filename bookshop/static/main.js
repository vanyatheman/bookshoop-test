console.log("Sanity check!");

// Get Stripe publishable key
fetch("/cart/config/")
.then((result) => result.json())
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // Event handler
  document.querySelector("#submitBtn").addEventListener("click", () => {
    const cartId = document.querySelector("#submitBtn").dataset.cartId; // Assuming you have cart ID stored in a data attribute

    // Get Checkout Session ID
    fetch("/cart/create-checkout-session/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')  // Ensure CSRF token is included
      },
      body: JSON.stringify({ cart_id: cartId })
    })
    .then((result) => {
      if (!result.ok) {
        return result.text().then(text => { throw new Error(text) });
      }
      return result.json();
    })
    .then((data) => {
      if (data.sessionId) {
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({ sessionId: data.sessionId });
      } else {
        console.error('Error:', data.error);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  });
});

// Function to get CSRF token from cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
