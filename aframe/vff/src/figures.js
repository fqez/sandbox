// Simple JS file for figures.html

// We need the A-frame library
// import 'aframe';

// Require font files to have them included in dist
// import roboto_json from './Roboto-msdf.json';
// import roboto_png from './Roboto-msdf.png';
// // URJC object
// import urjc_object from './urjc.obj';

// function foo() {
//   // var lines = new Array();
//   var i, p;
//   let l;
//   var s= "#line";
//   for (i = 0; i <180; i++) {
//     p = s + i.toString();
//     l = document.querySelector(p);
//     // lines.push(l);
//     l.addEventListener('mouseenter', bar(l));
//     l.addEventListener('mouseleave', bar2(l));
//   };
//   var tx = document.createElement('a-text');
//   var scene = document.querySelector('a-scene');
//   function bar(l) {
//     return function() {
//       var r = l.getAttribute('line').end;
      
//       l.setAttribute('line', "color: white");
//       tx.setAttribute('value' ,"1");
//       tx.setAttribute('scale' ,"0.8 0.8 0.8");
//       tx.setAttribute('position' , r);
//       tx.setAttribute('color', "#c58714");
//       scene.appendChild(tx);
  
//     };
//   };
  
//   function bar2(l) {
//     return function() {
//       l.setAttribute('line', "color: blue");
//       scene.removeChild(tx);

//     };
//   };
// };

var i = 0;
var j = 0;

function carInfo () {
  var car = document.querySelector('#car_chassis');
  var scene = document.querySelector('a-scene');
  var linC = document.querySelector('#linCar');
  var car1 = document.createElement('a-text');
  var car2 = document.createElement('a-text');
  var tx = document.querySelector('#vel');
  var hover = document.querySelector('#car_chassis-hover');

  document.addEventListener('keydown', function(event) {
    if (event.code == "KeyQ") {
      i += 0.1;
      j += 0.01;
    } else if (event.code == "KeyZ") {
      i -= 0.1;
      j -= 0.01;
    }
    tx.setAttribute('value', i.toFixed(2).toString() +" m/s \n "+ j.toFixed(3).toString() +" rad/s \n 00:00.000");
    car2.setAttribute('value', "Current V: "+i.toFixed(2).toString()+ "m/s \n Current W: "+j.toFixed(3).toString()+" rad/s");
    console.log(i,j);
  });
  
  car.addEventListener('mouseenter', function () {
    // car.setAttribute('scale', {x: 4, y: 4, z: 4});

    car1.setAttribute('id', "car_title");
    car1.setAttribute('value' ,"Formula 1");
    car1.setAttribute('scale' ,"0.8 0.8 0.8");
    car1.setAttribute('position' ,{x: 1.2, y: 2, z: 0});
    car1.setAttribute('color', "#c58714");

    car2.setAttribute('id', "description");
    car2.setAttribute('value' ,"Current V: 0 m/s \n Current W: 0 rad/s");
    car2.setAttribute('scale' ,"0.5 0.5 0.5");
    car2.setAttribute('position' ,{x: 1.2, y: 1.7, z: 0});
    car2.setAttribute('color', "#ffffff");


    linC.setAttribute('visible', true);
    hover.setAttribute('visible', "true");
    // el1.setAttribute('value' ,"Just a simple test");
    scene.appendChild(car1);
    scene.appendChild(car2);

  });

  car.addEventListener('mouseleave', function () {
    // car.setAttribute('scale', {x: 1, y: 1, z: 1});
    scene.removeChild(car1);
    scene.removeChild(car2);
    hover.setAttribute('visible', false);

    linC.setAttribute('visible', false);
  });
};


// Actual code for the application
function activate () {
  var lsr = document.querySelector('#laser1');
  var scene = document.querySelector('a-scene');
  var linL = document.querySelector('#linLaser');
  var el1 = document.createElement('a-text');
  var el2 = document.createElement('a-text');
  
  lsr.addEventListener('mouseenter', function () {
    lsr.setAttribute('scale', {x: 4, y: 4, z: 4});

    el1.setAttribute('id', "description");
    el1.setAttribute('value' ,"Hokuyo Laser");
    el1.setAttribute('scale' ,"0.8 0.8 0.8");
    el1.setAttribute('position' ,{x: 3, y: 1.2, z: 0});
    el1.setAttribute('color', "#c58714");

    el2.setAttribute('id', "description");
    el2.setAttribute('value' ,"Min. Range: 0.01 m\n Max. Range: 10.0 m \n Min. Angle: 0 deg. \n Max. Angle: 180 deg.");
    el2.setAttribute('scale' ,"0.5 0.5 0.5");
    el2.setAttribute('position' ,{x: 3, y: 0.8, z: 0});
    el2.setAttribute('color', "#ffffff");


    linL.setAttribute('visible', true);
    // el1.setAttribute('value' ,"Just a simple test");
    scene.appendChild(el1);
    scene.appendChild(el2);

  });

  lsr.addEventListener('mouseleave', function () {
    lsr.setAttribute('scale', {x: 1, y: 1, z: 1});
    // var text = document.querySelector('#description');
    scene.removeChild(el1);
    scene.removeChild(el2);

    linL.setAttribute('visible', false);
  });
};


document.addEventListener('DOMContentLoaded', activate);
document.addEventListener('DOMContentLoaded', carInfo);

// document.addEventListener('DOMContentLoaded', foo);


// document.addEventListener("DOMContentLoaded", function(event) {
//   console.log("DOM fully loaded and parsed");

//   var el = document.querySelector('#laser1');
//   el.emit('anEvent');

//   var scene = document.querySelector('a-scene');

  


  // <a-text value="Just a simple test" color="red"
  //       position="-3.5 0.5 -2" rotation="-45 30 0" scale="2.5 2.5 2.5" font="Roboto-msdf.json"></a-text>
  


  // var el1 = document.createElement('a-entity');
  // el1.setAttribute('geometry', {
  //   primitive: 'box',
  //   height: 3,
  //   width: 1
  // });
  // scene.appendChild(el1);
// });