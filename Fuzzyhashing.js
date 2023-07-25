import fetch from 'node-fetch';

const { createCanvas, loadImage } = require('canvas');
const fetch = require('node-fetch');
const cheerio = require('cheerio');

async function fetchWebsiteAndProcessImages(websiteUrl) {
  try {
    const response = await fetch(websiteUrl);
    const htmlContent = await response.text();
    const imageUrls = extractImageUrlsFromHTML(htmlContent);
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
  const cheerio = require('cheerio');

// Rest of your code...

function extractImageUrlsFromHTML(htmlContent) {
  // Load the HTML content using cheerio
  const $ = cheerio.load(htmlContent);

  // Initialize an array to store the image URLs
  const imageUrls = [];

  // Extract image URLs from the img tags
  $('img').each((index, element) => {
    const src = $(element).attr('src');
    if (src) {
      imageUrls.push(src);
    }
  });

  // Extract image URLs from div, a, and span background images
  $('div, a, span').each((index, element) => {
    const bg = $(element).css('background-image');
    const imageUrl = bg.replace('url(','').replace(')','').replace(/\"/gi, "");
    if (imageUrl && imageUrl !== 'none') {
      imageUrls.push(imageUrl);
    }
  });

  // Extract image URLs from svg elements
  $('svg').each((index, element) => {
    // Wrap svg in new <svg><foreignObject> element
    const svgHtml = $.html(element);
    const wrapperOpen = '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="200">' +
                       '<foreignObject width="100%" height="100%">';
    const wrapperClose = '</foreignObject></svg>';
    const dataString = wrapperOpen + svgHtml + wrapperClose;

    // Assuming you only want to include SVGs as image URLs
    // (you can adjust this based on your requirements)
    imageUrls.push('data:image/svg+xml;charset=utf8,' + encodeURIComponent(dataString));
  });


  return [
    'https://www.tmz.com/image1.jpg',
    'https://www.tmz.com/image2.jpg',
    // Add more image URLs as needed.
  ];}

}
async function processImageUsingAHash(imageUrl) {
    try {
      const response = await fetch(imageUrl);
      const buffer = await response.buffer();
      const img = await loadImageAsync(buffer);
      const hash = aHash(img);
      console.log('Image hash:', hash);
    } catch (error) {
      console.error('Error fetching or processing image:', error);
    }
  }
  
var aHash = function (img) {
  var width = 25,
    height = 25,
    hash_padding = 3; // Pad resulting hash up to proper hash length
  var canvas = createCanvas(width, height),
    ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0, width, height);
  var im = ctx.getImageData(0, 0, width, height);
  // Rest of the aHash function implementation...
  return 'aHashValue'; // Return the actual hash value as needed.
};
async function loadImageAsync(url) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = url;
    });
  }
  
// URL of the website you want to process
const websiteUrl = 'https://www.tmz.com';
// Call the function to fetch the website and process its images
fetchWebsiteAndProcessImages(websiteUrl);