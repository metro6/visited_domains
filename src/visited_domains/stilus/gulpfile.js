// Load plugins
var gulp = require('gulp'),
pug = require('gulp-pug'),
stylus = require('gulp-stylus'),
watch = require('gulp-watch'),
sourcemaps = require('gulp-sourcemaps'),
autoprefixer = require('autoprefixer-stylus'),
rename = require("gulp-rename"),
cssmin = require('gulp-clean-css'),
plumber = require('gulp-plumber'),
connect = require('gulp-connect'),
locals = require('./locals.json');

//start localhost
gulp.task('connect', function () {
    var new_port = 3001;
    tcpPortUsed.check(new_port, '127.0.0.1')
    .then(function(inUse) {
      if (inUse) {
        new_port = 3011;
      }
      connect.server({
          root: '',
          port: new_port,
          livereload: true
      });
    }, function(err) {
      console.error(err.message);
    });
});

//start localhost
gulp.task('connect', function () {
connect.server({
root: '',
port: 3005,
livereload: true
});
});

//path
var path_file = {
build: {
  stylus: '../static/dist/css/',
},
src: {
  stylus: './src/css/*.styl',
},
watch: {
  stylus: 'src/css/*.styl',
}
};

gulp.task('stylus:build', function () {
  return gulp.src(path_file.src.stylus)
    .pipe(plumber({
      errorHandler: function (error) {
        console.log(error.message);
        this.emit('end');
    }}))
    .pipe(sourcemaps.init())
    .pipe(stylus({
      'use': [autoprefixer({ browsers: ['last 5 versions'] })],
    }))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(path_file.build.stylus))
    .pipe(connect.reload());
});

gulp.task('build', [
'stylus:build',
]);

gulp.task('watch', function(){
watch([path_file.watch.stylus], function(event, cb) {
gulp.start('stylus:build');
});
});

gulp.task('default', ['connect','build', 'watch']);
