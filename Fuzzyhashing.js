const { createCanvas, loadImage } = require('canvas');

var aHash = function(img) {
  var width = 25,
  height = 25,
  hash_padding = 3; // Pad resulting hash up to proper hash length

  var canvas = document.createElement('canvas'),
      ctx = canvas.getContext('2d');

  canvas.width = width;
  canvas.height = height;
  ctx.drawImage(img, 0, 0, width, height);
  var im = ctx.getImageData(0, 0, width, height);

  var num_channels = 4;
  var vals = new Float64Array(width * height);

  // Convert image to grayscale
  for(var i = 0; i < width; i++){
      for(var j = 0; j < height; j++){
          var base = num_channels * (width * j + i);
          if (im.data[base+3]  == 0) {
              vals[width * j + i] = 255;
              continue
          }
          vals[width * j + i] = 0.2126 * im.data[base] +
              0.7152 * im.data[base + 1] +
              0.0722 * im.data[base + 2];
      }
  }

  // Find average pixel value,
  var pixel_sum = 0;
  for (var i = 0; i < vals.length; i++) {
      pixel_sum += vals[i];
  }
  var pixel_avg = pixel_sum / vals.length;

  var hash = '';

  // Add padding to start of hash:
  for (var i = 0; i < hash_padding; i++) {
      hash += 0;
  }

  for (var i = 0; i < width; i++) {
      for (var j = 0; j < height; j++) {
          var pixel = vals[width * j + i];
          hash += pixel < pixel_avg ? 1 : 0;
      }
  }
  if (VERBOSE) {
    console.log(hash);
  }
  return hash;
};

// Receives two images and determines whether one image is a subset of the other.
function isSubset(subsetImg, fullImg) {
  var subsetHash = aHash(subsetImg);
  var fullHash = aHash(fullImg);

  // Compare the hashes of the two images to check if the subset image matches part of the full image.
  var sim_score = 1 - distance(subsetHash, fullHash) / 628.0;

      console.log("Sim score: " + sim_score);
  

  // Adjust the threshold value (SIM_THRESHOLD) based on your requirements to determine the match.
  var SIM_THRESHOLD = 0.9;

  // If the similarity score is above the threshold, the subsetImg is a subset of the fullImg.
  return sim_score > SIM_THRESHOLD;
}

var subsetImage = loadImage("taboola.png");
var fullImage = loadImage("adv.png");


// Wait for the images to load before performing the comparison
// subsetImage.onload = function() {
//   fullImage.onload = function() {
//       var isSubsetImage = isSubset(subsetImage, fullImage);
//       if (isSubsetImage) {
//           console.log("The subset image is a subset of the full image.");
//       } else {
//           console.log("The subset image is not a subset of the full image.");
//       }
//   };
// };
Promise.all([subsetImage, fullImage]).then(images => {
  var isSubsetImage = isSubset(images[0], images[1]);
  if (isSubsetImage) {
    console.log("The subset image is a subset of the full image.");
  } else {
    console.log("The subset image is not a subset of the full image.");
  }
}).catch(err => {
  console.error("Error loading images:", err);
});