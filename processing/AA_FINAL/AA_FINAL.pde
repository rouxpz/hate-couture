import processing.pdf.*;
import toxi.color.*;
import toxi.util.datatypes.*;

int id; //id number for each speech instance
int pixelid; //id number for each pixel
int counter = 0; //counts the pixels in base image to assign the pixel id

float h; //hue of the fill
float s; //saturation of the fill
float b; //brightness of the fill

ArrayList<Pixels> squares = new ArrayList(); //array list for pixels
ArrayList<Speech> scores = new ArrayList(); //array list for 

PImage cloth;

void setup() {
  size(80, 1214);
  
  beginRecord(PDF, "test.pdf");
  
  cloth = loadImage("aa-fabric.png");
  
  colorMode(HSB, 1, 1, 1);
  
  loadData();
  countPixels();
  
  for (Speech sp:scores) {
    for (Pixels pi:squares) {
      if (sp.id == pi.id) {
        println(sp.score);
        write(sp.assign);
        noStroke();
        TColor shade = TColor.newHSV(h, s, b);
        fill(shade.hue(), shade.saturation(), shade.brightness());
        rect(pi.x, pi.y,1,1);
      }
    }
  }
}

//nothing here
void draw() {
}

//loads the data and assigns qualities to each instance
void loadData() {
  String[] rows = loadStrings("nigger-final.csv");
  
  //for (int i = 0; i < 1000; i++) {
  for (int i = 0; i < 97086; i++) {
    if (rows[i] != null) {
      String[] lines = split(rows[i], ',');
      
      Speech s = new Speech();
      s.id = i;
      s.score = float(lines[0]);
      
      if(s.score <= 2.5) {
        s.assign = 0;
      } else if (s.score > 2.5 && s.score <= 6) {
        s.assign = 1;
      } else if (s.score > 6 && s.score <= 10) {
        s.assign = 2;
      } else if (s.score > 10 && s.score <= 15) {
        s.assign = 3;
      } else if (s.score > 15) {
        s.assign = 4;
      }
      
      //println(s.score);
      scores.add(s);
      
    }
  }
}

//assigns pixels to class & gives each an ID
void countPixels() {
  loadPixels();
  cloth.loadPixels();
  
  for (int x = 0; x < width; x++) {
    for (int y = 0; y < height; y++) {
      
      int loc = x+y*(width);
      
      if (cloth.pixels[loc] <= 100) {
        Pixels p = new Pixels();
        p.x = x;
        p.y = y;
        p.id = counter;
        //println(p.id);
        squares.add(p);
       
        counter++;
      }
    }
  }
  
}

//determines colors
void write(int level) {
  
  if (level == 4) {
    h = 0;
    b = 0.16;
    s = 0;
  } else if (level == 3) {
    h = 0;
    b = 0.33;
    s = 0;
  } else if (level == 2) {
    h = 0;
    b = 0.49;
    s = 0;
  } else if (level == 1) {
    h = 0;
    b = 0.66;
    s = 0;
  } else if (level == 0) {
    h = 0;
    b = 0.82;
    s = 0;
  }
}

//saves PDF
void keyPressed() {
  endRecord();
}

