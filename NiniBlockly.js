function shootIfEnemy(angle) {
  if (scan(angle) != Infinity) {
    cannon(angle, scan(angle)); 
  }
}

function RUN() {
  if (previous_health > health()) {
    let i = 1;
    const random_direction = Math.random() * 360
    while (i++ < 200) { /* use a counter to limit move time */
      swim(random_direction)
    }
    stop();
    previous_health = health();
  }
}

let range;
let previous_health = health();
let angle = Math.random() * 360;
let res = 2;
let swim_stuff = 8;

while (true) { 
  swim(swim_stuff)
  
  while ((range = scan(angle, res)) != Infinity) {
    if (range > 70) { /* out of range, head toward it */
      // drive(angle, 50);
      // var i = 1;
      // while (i++ < 50) /* use a counter to limit move time */
      //   ;
      // drive(angle, 0);
      angle -= 3;
    } else {
      stop();
      cannon(angle, range);
      angle -= 15;
    }
  }
  angle += res;
  angle %= 360;
  
  swim_stuff = swim_stuff - 0.8
}

// var range;
// var last_dir = 0;

// var res = 2;
// let previous_health = health();
// var angle = Math.random() * 360;
// while (true) {
//   while ((range = scan(angle, res)) != Infinity) {
//     if (range > 70) { /* out of range, head toward it */
//       drive(angle, 50);
//       var i = 1;
//       while (i++ < 50) /* use a counter to limit move time */
//         ;
//       drive (angle, 0);
//       if (previous_health != health()) {
//         previous_health = health();
//         run();
//       }
//       angle -= 3;
//     } else {
//       while (!cannon(angle, range))
//         ;
//       if (previous_health != health()) {
//         previous_health = health();
//         run();
//       }
//       angle -= 15;
//     }
//   }
//   if (previous_health != health()) {
//     previous_health = health();
//     run();
//   }
//   angle += res;
//   angle %= 360;
// }

// function run() {
//   let i = 1;
//   const random_direction = Math.random() * 360
//   while (i++ < 200) { /* use a counter to limit move time */
//       swim(random_direction)
//     }
//     stop()
// }
