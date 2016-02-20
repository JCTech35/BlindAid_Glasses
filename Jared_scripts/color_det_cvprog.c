/* =========================================================================
* Created by: Jared Charter and Ryan Brinkley
* ECE 438 Final Project: The Sound of Color
* Last modified: 12/14/2015
****************************************************************************/
/*
** include header files
*/
#include "CVIPtoolkit.h"
#include "CVIPconvert.h"
#include "CVIPdef.h"
#include "CVIPimage.h"
#include "CVIPlab.h"
#include "CVIPgeometry.h"
#include "fuzzyc.h"
#include "hist_thresh.h"
#include <CVIPspfltr.h>
//#include "median_cut.h" //made own median_cut_custom.c file
#include <stdio.h>
#include <string.h>
#include <Windows.h>
#define SPEC_COLORS 14;
#define COLOR_SHADES 9;
//Image object for input
Image *input();
/*Structure for each color
Members:
-----------
Color name
Color shades (array of color structs)
Color frequency */
struct Spectrum{
char* name;
Color color[9];
int freq;
};
// start main funct
void main_cviplab(){
IMAGE_FORMAT format; /* the input image format */
Image *cvipImage; /* pointer to the CVIP Image structure */
Image *cvipImageOut; /* pointer to the CVIP Image structure */
char *outputfile; /* output file name */
CVIP_BOOLEAN done = CVIP_NO;
//Image middle to crop from
int cropRowOffset = 980;
int cropColOffset = 1264;
int cropRows = 64;
int cropCols = 64;
int i,j,g,b; //iterators
//Initilize differences(distances)
int minDiff = 1000;
int minDiffIndex = 0;
//Default background for median_cut
Color bg = {0, 0, 0};
//Pointer for storing object color array
int *maxColors;
//array for storing calculated differences
int diff[14][9];
//array for storing grey differences
int greyDiff[3];
int isgrey = 0;//flag for grey color
//Structure of all 14 colors
struct Spectrum spectrum [14] = {
{"white",
{{ 224 , 224 , 224 },
{ 224 , 224 , 224 },
{ 224 , 224 , 224 },
{ 255 , 255 , 255 },
{ 255 , 255 , 255 },
{ 255 , 255 , 255 },
{ 255 , 255 , 255 },
{ 255 , 255 , 255 },
{ 255 , 255 , 255 }}, 1000},
{"pink",
{{ 51 , 0 , 51 },
{ 102 , 0 , 102 },
{ 153 , 0 , 153 },
{ 204 , 0 , 204 },
{ 255 , 0 , 255 },
{ 255 , 51 , 255 },
{ 255 , 102 , 255 },
{ 255 , 153 , 255 },
{ 255 , 204 , 255 }}, 946},
{"magenta",
{{ 51 , 0 , 25 },
{ 102 , 0 , 51 },
{ 153 , 0 , 76 },
{ 204 , 0 , 102 },
{ 255 , 0 , 127 },
{ 255 , 51 , 153 },
{ 255 , 102 , 178 },
{ 255 , 153 , 204 },
{ 255 , 204 , 229 }}, 892},
{"red",
{{ 51 , 0 , 0 },
{ 102 , 0 , 0 },
{ 153 , 0 , 0 },
{ 204 , 0 , 0 },
{ 255 , 0 , 0 },
{ 255 , 51 , 51 },
{ 255 , 102 , 102 },
{ 255 , 153 , 153 },
{ 255 , 204 , 204 }}, 838},
{"orange",
{{ 51 , 25 , 0 },
{ 102 , 51 , 0 },
{ 153 , 76 , 0 },
{ 204 , 102 , 0 },
{ 255 , 128 , 0 },
{ 255 , 153 , 51 },
{ 255 , 178 , 102 },
{ 255 , 204 , 153 },
{ 255 , 229 , 204 }}, 785},
{"yellow",
{{ 51 , 51 , 0 },
{ 102 , 102 , 0 },
{ 153 , 153 , 0 },
{ 204 , 204 , 0 },
{ 255 , 255 , 0 },
{ 255 , 255 , 51 },
{ 255 , 255 , 102 },
{ 255 , 255 , 153 },
{ 255 , 255 , 204 }}, 731},
{"lime",
{{ 25 , 51 , 0 },
{ 51 , 102 , 0 },
{ 76 , 153 , 0 },
{ 102 , 204 , 0 },
{ 128 , 255 , 0 },
{ 153 , 255 , 51 },
{ 178 , 255 , 102 },
{ 204 , 255 , 153 },
{ 229 , 255 , 204 }}, 677},
{"green",
{{ 0 , 51 , 0 },
{ 0 , 102 , 0 },
-3-
{ 0 , 153 , 0 },
{ 0 , 204 , 0 },
{ 0 , 255 , 0 },
{ 51 , 255 , 51 },
{ 102 , 255 , 102 },
{ 204 , 255 , 153 },
{ 229 , 255 , 204 }}, 623},
{"aqua",
{{ 0 , 51 , 25 },
{ 0 , 102 , 51 },
{ 0 , 153 , 76 },
{ 0 , 204 , 102 },
{ 0 , 255 , 128 },
{ 51 , 255 , 153 },
{ 102 , 255 , 178 },
{ 153 , 255 , 204 },
{ 204 , 255 , 229 }}, 569},
{"lightblue",
{{ 0 , 51 , 51 },
{ 0 , 102 , 102 },
{ 0 , 153 , 153 },
{ 0 , 204 , 204 },
{ 0 , 255 , 255 },
{ 51 , 255 , 255 },
{ 102 , 255 , 255 },
{ 153 , 255 , 255 },
{ 204 , 255 , 255 }}, 515},
{"blue",
{{ 0 , 25 , 51 },
{ 0 , 51 , 102 },
{ 0 , 76 , 153 },
{ 0 , 102 , 204 },
{ 0 , 128 , 255 },
{ 51 , 153 , 255 },
{ 102 , 178 , 255 },
{ 153 , 204 , 255 },
{ 204 , 229 , 255 }}, 462},
{"deepblue",
{{ 0 , 0 , 51 },
{ 0 , 0 , 102 },
{ 0 , 0 , 153 },
{ 0 , 0 , 204 },
{ 0 , 0 , 255 },
{ 51 , 51 , 255 },
{ 102 , 102 , 255 },
{ 153 , 153 , 255 },
{ 204 , 204 , 255 }}, 408},
{"purple",
{{ 25 , 0 , 51 },
{ 51 , 0 , 102 },
{ 76 , 0 , 153 },
{ 102 , 0 , 204 },
{ 127 , 0 , 255 },
{ 153 , 51 , 255 },
{ 178 , 102 , 255 },
{ 204 , 153 , 255 },
{ 229 , 204 , 255 }}, 354},
{"black",
{{ 0 , 0 , 0 },
{ 32 , 32 , 32 },
{ 32 , 32 , 32 },
{ 32 , 32 , 32 },
{ 32 , 32 , 32 },
{ 32 , 32 , 32 },
{ 32 , 32 , 32 },
{ 32 , 32 , 32 },
{ 32 , 32 , 32 }}, 300}};
while(!done) {
print_CVIP("\n\nImage>>");
/*Get the input image */
cvipImage = input();
if(cvipImage == NULL)
{
error_CVIP("main", "could not read input image");
break;
}
//for dynamic image size
//cropRowOffset = ((getNoOfRows_Image(cvipImage))/2)-32;
//cropColOffset = ((getNoOfCols_Image(cvipImage))/2)-32;
cvipImage = crop(cvipImage,cropRowOffset,cropColOffset,cropRows,cropCols); //crop
64x64 image from center
cvipImage = mean_filter(cvipImage, 9); //apply 9x9 mask mean filter
cvipImage = median_cut_segment(cvipImage,8,CVIP_NO, bg); //segment into 8 colors
print_CVIP("\n");
//retreives the RGB values and count of this color output from the median_cut
segmentation
maxColors = get_MaxColorValsPlease();
/*This loop calculates the distance to each color and stores it in the diff[][] array.
It first finds the distance to each color's shade using a city-block distance
metric, then
it checks to see if any of these distances are the new smallest distance. If so,
the distance value and
color it is contained in is stored as the minDiff and minDiffIndex. THEY ARE EQUAL!
is printed when a
distance of the same value as the current minDiff is found. Once completed theminDiff will contain the
value of the minimum distance and the minDiffIndex will be the index of the
spectrum structre array which
has the color name and frequency. */
minDiff = 1000;
for(i=0;i<14;i++){
for(j=0;j<9;j++){
diff[i][j] = abs(maxColors[0] - spectrum[i].color[j].r) + abs(maxColors[1] -
spectrum[i].color[j].g) + abs(maxColors[2] - spectrum[i].color[j].b);
if (diff[i][j] < minDiff){
minDiff = diff[i][j];
minDiffIndex = i;
print_CVIP("\nDistance: %d for Color: %d, %d, %d", minDiff,spectrum[i].color
[j].r,
spectrum[i].color[j].g, spectrum[i].color[j].b);
}
else if(diff[i][j] == minDiff)
print_CVIP("\nTHEY ARE EQUAL!");
//For debugging:
//print_CVIP("\nDistance: %d for Color: %d %d %d", diff[i][j],
spectrum[i].color[j].r, spectrum[i].color[j].g, spectrum[i].color[j].b);
}
}//endfor
//Each grey distance is calculated individually and stored in the greyDiff array. The
grey RGB values check against
// are the repititions of each of the objects RGB values. For example, (54, 54, 54).
isgrey = 0;
greyDiff[0] = abs(maxColors[0] - maxColors[0]) + abs(maxColors[1] - maxColors[0]) + abs(
maxColors[2] - maxColors[0]);
greyDiff[1] = abs(maxColors[0] - maxColors[1]) + abs(maxColors[1] - maxColors[1]) + abs(
maxColors[2] - maxColors[1]);
greyDiff[2] = abs(maxColors[0] - maxColors[2]) + abs(maxColors[1] - maxColors[2]) + abs(
maxColors[2] - maxColors[2]);
//This loop checks if the grey values are closer than the current minDiff and if the
color is closer to grey than the
// current selected color.
for (g = 0; g<3;g++){
print_CVIP("\nGrey diff is: %d", greyDiff[g]);
if ((greyDiff[g] <= 30) && (greyDiff[g] < minDiff)){
isgrey = 1;
}//endif
}//endfor
//Print the color which is selected and its frequency. Or print if grey (no freq)
print_CVIP("\n\nMajority Color: %d, %d,%d,%d", maxColors[0],maxColors[1], maxColors[2],
maxColors[3]);
if(isgrey == 0){
print_CVIP("\nThe color is: %s which is frequency: %d Hz", spectrum[minDiffIndex].
name,spectrum[minDiffIndex].freq);
Beep(spectrum[minDiffIndex].freq,2000);
}
else if (isgrey == 1){print_CVIP("\nThe color is: grey");}
//play all the color sounds
/*for(b = 0; b < 14; b++){
printf("\n %s", spectrum[b].name);
Beep(spectrum[b].freq,1500);
}*/
//display the resultant image
view_Image(cvipImage,"Cropped_Area");
//delete_Image (cvipImage);
}//endwhile
}
/*
**end of the function main
/*
** The following function reads in the image file specified by the user,
** stores the data and other image info. in a CVIPtools Image structure,
** and displays the image.
*/
Image* input(){
char *inputfile;
Image *cvipImage;
/*
** get the name of the file and stores it in the string 'inputfile '
*/
print_CVIP("\n\t\tEnter the Input File Name: ");
inputfile = getString_CVIP();
/*
** creates the CVIPtools Image structure from the input file
*/
cvipImage = read_Image(inputfile, 1);
if(cvipImage == NULL) {
error_CVIP("init_Image", "could not read image file");
free(inputfile);
return NULL;
}
/*
** display the source image
*/
//view_Image(cvipImage,inputfile);
/*
**IMPORTANT: free the dynamic allocated memory when it is not needed
*/
free(inputfile);
return cvipImage;
}


median_cut_custom.c
Function modified:
Image *
median_cut_segment(	Image *imgP,	int newcolors,	CVIP_BOOLEAN is_bg,	Color bg)
{
	byte **cvecP, mask;
	register byte *rP, *gP, *bP;
	unsigned imgsize, no_pixels = 0;
    	int rows, cols;
    	register int i;
    	register int ind;
	Color pixel;
	ColorMap colormap;
	ColorHistogram *chP, *newchP;
	ColorHashTable *chtP;
	const char *fn = "median_cut_segment";

	chP = new_ColorHist();

	mask = MAXPIXVAL;

	rows = getNoOfRows_Image(imgP);
	cols = getNoOfCols_Image(imgP);
	imgsize = rows*cols;

	cvecP = (byte **) malloc(3*sizeof(byte *));
	getBandVector_Image(imgP, cvecP);

	/*
	** Step 2: attempt to make a histogram of the colors, unclustered.
	** If at first we don't succeed, lower maxval to increase color
	** coherence and try again.  This will eventually terminate, with
	** maxval at worst 15, since 32^3 is approximately MAXCOLORS.
	*/
	for(;;) {

		msg_CVIP(fn, "making histogram...\n" );
		compute_ColorHist(chP, imgP, MAXCOLORS);
	    	if (chP->histogram != NULL)
			break;
		mask <<= 1;
	    	msg_CVIP(fn, "too many colors!\n" );
	    	msg_CVIP(fn, "reducing pixel sample range to [%u - %u] to improve clustering...\n", ((byte) ~mask)+1, mask);
		rP = cvecP[0];
		gP = cvecP[1]; 
		bP = cvecP[2];
	    	for(i = 0; i < imgsize; i++, rP++, gP++, bP++ ) {
			*rP &= mask;
			*gP &= mask;
			*bP &= mask;
		}
	}
	msg_CVIP(fn, "%u colors found\n", chP->no_of_colors );	

	if(is_bg)
		dropColor_ColorHist(chP, bg, &no_pixels); 

	/*
	** Step 3: apply median-cut to histogram, making the new colormap.
	*/
	msg_CVIP(fn, "choosing %d colors...\n", newcolors );
	newchP = mediancut( chP, imgsize - no_pixels, newcolors );
	colormap = newchP->histogram;
	delete_ColorHist(chP);
   

    	/*
   	** Step 4: map the colors in the image to their closest match in the
    	** new colormap, and write 'em out.
    	*/

    	msg_CVIP(fn, "mapping image to new colors...\n" );

    	chtP = new_ColorHT();

	rP = cvecP[0];
	gP = cvecP[1];
	bP = cvecP[2];
	
    	for (i = 0; i < imgsize; i++, rP++, gP++, bP++ ) {
	
		/* 
		 * Check hash table to see if what we have already matched this
		 * color. 
		 */

		
		assign_Color(pixel,*rP,*gP,*bP);

		if(is_bg && equal_Color(pixel,bg)) continue;

		ind = lookUpColor_ColorHT( chtP, pixel );

	   	if ( ind == -1 ) { /* search colormap for closest match. */

			register int j, r, g, b;
			register long dist, newdist;

			dist = 2000000000;

			for (j = 0; j < newcolors; j++) {

		    		r = getRed_Color( colormap[j].pixel );
		    		g = getGrn_Color( colormap[j].pixel );
		    		b = getBlu_Color( colormap[j].pixel );
		    		newdist = ( *rP - r ) * ( *rP - r ) +
			      	  	  ( *gP - g ) * ( *gP - g ) +
			      	  	  ( *bP - b ) * ( *bP - b );
		    		if ( newdist < dist ) {
					ind = j;
					dist = newdist;
				}

		    	}

		   	addObject_ColorHT(chtP, pixel, ind);
		}	

	    	*rP = getRed_Color(colormap[ind].pixel);
		*gP = getGrn_Color(colormap[ind].pixel);
		*bP = getBlu_Color(colormap[ind].pixel);
		
		colormap[ind].value++;
	}


print_CVIP("IN MEDIAN SEGMENT! WOO!");
//print_ColorHist(newchP);
colorTemp = print_ColorHist_MaxColor(newchP);
colorArray[0] = colorTemp[0];
colorArray[1] = colorTemp[1];
colorArray[2] = colorTemp[2];
colorArray[3] = colorTemp[3];
delete_ColorHT(chtP);
delete_ColorHist(newchP);
//print_CVIP("\nHERE THEY STAY: %d,%d,%d,%d", colorArray[0],colorArray[1],colorArray[2],colorArray[3]);
free(cvecP);
return imgP;
}

Function added:
int* get_MaxColorValsPlease(){
	//print_CVIP("\nHERE THEY STAY STILL PLEASE: %d,%d,%d,%d", colorArray[0],colorArray[1],colorArray[2],colorArray[3]);
	return colorArray;
}









colormap_custom.c
Function added:
int* print_ColorHist_MaxColor( ColorHistogram *chP )
{
   register int i;
   const char *fn = "print";
   int redVal,greenVal,blueVal,totalVal;
   int valArray[4];
   if(!chP->histogram) return;

  /* Sort by count. */
   qsort( chP->histogram, chP->no_of_colors, sizeof(ColorHistObject), valueCompare );
   msg_CVIP(fn, "\nTOTAL NUMBER OF UNIQUE COLORS = %u.\n\n",chP->no_of_colors);
   msg_CVIP(fn, "RED GRN BLU\tCOUNT\n" );
   msg_CVIP(fn, "--- --- ---\t-----\n" );

   valArray[0] = getRed_Color(chP->histogram[0].pixel);
   valArray[1] = getGrn_Color(chP->histogram[0].pixel);
   valArray[2] = getBlu_Color(chP->histogram[0].pixel);
   valArray[3] = chP->histogram[0].value;

   for ( i = 0; i < chP->no_of_colors; i++ )
		msg_CVIP(fn, "%3d %3d %3d\t%d\n", getRed_Color(chP->histogram[i].pixel), getGrn_Color(chP->histogram[i].pixel), getBlu_Color(chP->histogram[i].pixel), chP->histogram[i].value );

   msg_CVIP(fn,"\n" );

   //print_CVIP("HERE THEY START: %d,%d,%d,%d", valArray[0],valArray[1],valArray[2],valArray[3]);
   return valArray;
}
