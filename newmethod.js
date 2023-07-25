async function fetchWebsiteAndProcessImages(websiteUrl) {
    try {
      // Fetch the HTML content of the website
      const response = await fetch(websiteUrl);
      const htmlContent = await response.text();
  
      // Extract the image URLs from the HTML content
      const imageUrls = extractImageUrlsFromHTML(htmlContent);
  
      // Process each image using the aHash function
      for (const imageUrl of imageUrls) {
        await processImageUsingAHash(imageUrl);
      }
    } catch (error) {
      console.error('Error fetching or processing images:', error);
    }
  }
  
  function extractImageUrlsFromHTML(htmlContent) {
    // Implement the logic to extract image URLs from the HTML content.
    // You can use regular expressions or DOM manipulation techniques to do this.
    // For demonstration purposes, assume there are some image URLs hardcoded here:
    // Replace these with the actual logic to extract image URLs from the TMZ website.
    return [
      'https://www.tmz.com/image1.jpg',
      'https://www.tmz.com/image2.jpg',
      // Add more image URLs as needed.
    ];
  }
  
  async function processImageUsingAHash(imageUrl) {
    try {
      // Fetch the image
      const response = await fetch(imageUrl);
      const blob = await response.blob();
  
      // Create an image element and set the image source to the fetched blob
      const img = new Image();
      img.src = URL.createObjectURL(blob);
  
      // Wait for the image to load
      await new Promise((resolve) => {
        img.onload = resolve;
      });
  
      // Call the aHash function with the loaded image
      aHash(img);
    } catch (error) {
      console.error('Error fetching or processing image:', error);
    }
  }
  

  var aHash = function(imgUrl) {
    var width = 25,
        height = 25,
        hash_padding = 3; // Pad resulting hash up to proper hash length

    var canvas = document.createElement('canvas'),
        ctx = canvas.getContext('2d');

    var img = new Image();
    img.crossOrigin = 'anonymous';

    img.onload = function() {
        canvas.width = width;
        canvas.height = height;
        ctx.drawImage(img, 0, 0, width, height);
        var im = ctx.getImageData(0, 0, width, height);

        var num_channels = 4;
        var vals = new Float64Array(width * height);

        // Convert image to grayscale
        for (var i = 0; i < width; i++) {
            for (var j = 0; j < height; j++) {
                var base = num_channels * (width * j + i);
                if (im.data[base + 3] == 0) {
                    vals[width * j + i] = 255;
                    continue;
                }
                vals[width * j + i] =
                    0.2126 * im.data[base] +
                    0.7152 * im.data[base + 1] +
                    0.0722 * im.data[base + 2];
            }
        }

        var pixel_sum = 0;
        for (var i = 0; i < vals.length; i++) {
            pixel_sum += vals[i];
        }
        var pixel_avg = pixel_sum / vals.length;

        var hash = '';

        // Add padding to the start of the hash:
        for (var i = 0; i < hash_padding; i++) {
            hash += '0';
        }

        for (var i = 0; i < width; i++) {
            for (var j = 0; j < height; j++) {
                var pixel = vals[width * j + i];
                hash += pixel < pixel_avg ? '1' : '0';
            }
        }

        // The hash is ready, you can use it as needed.
        console.log('Image hash:', hash);
    };

    img.src = imgUrl; // Load the image from the provided URL
};
  // Rest of the aHash function and other utility functions...
  // (Same as in the previous code)
  
  // Example usage:
  
  // URL of the website you want to process
  const websiteUrl = 'https://www.tmz.com';
  
  // Call the function to fetch the website and process its images
  fetchWebsiteAndProcessImages(websiteUrl);
  