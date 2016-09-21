// var socket = io(); // eslint-disable-line

// /** Configure development environment: */
// socket.on('BROWSER_REFRESH_URL', function(BROWSER_REFRESH_URL) { // eslint-disable-line
//   // console.log('connected: ' + BROWSER_REFRESH_URL);
//   // Quick fix: http://stackoverflow.com/a/611016
//   var script = document.createElement('script'); // eslint-disable-line
//   script.src = BROWSER_REFRESH_URL;
//   $('body').append(script);
// });

// /**
//  * RESPOND to events:
//  */
// socket.on('new-photo', function(newPath) { // eslint-disable-line
//   $('#device-img').attr('src', `/photos/${newPath}`);
// });
// socket.on('step', function(num, newStatus) { // eslint-disable-line
//   num.forEach(function(element) { // eslint-disable-line
//     // console.log('a[' + index + '] = ' + element + ' - with ' + newStatus);
//     var stepID = `#Step ${element}`; // eslint-disable-line
//     $(stepID).attr('class', newStatus);
//   });
// });
