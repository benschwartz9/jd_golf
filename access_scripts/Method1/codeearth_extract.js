var dataset = ee.ImageCollection('USDA/NAIP/DOQQ')
                  .filter(ee.Filter.date('2015-08-12', '2020-08-12'));
var trueColor = dataset.select(['R', 'G', 'B']);
var trueColorVis = {
  min: 0.0,
  max: 255.0,
};
Map.setCenter(-86.92444046924065, 40.43876508216534, 17);
Map.addLayer(trueColor, trueColorVis, 'True Color');

var final_image = dataset.median()

// Export the image to an Earth Engine asset.
Export.image.toDrive({
  image: final_image,
  description: 'both_png',
  scale: 0.1,
  region: myregion,
  maxPixels: 1e13,
  format: "png"
});