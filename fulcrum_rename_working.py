import arcpy, os, shutil


#Specify inputs


siteFeatures = "H:/fulcrum/swppp_inspect/swppp_inspect.gdb/swppp_inspect"
wtFeatures = "H:/fulcrum/swppp_inspect/swppp_inspect.gdb/swppp_inspect_walkthrough"
targetDir = "H:/fulcrum/sitedocs/"

#derive source directory from fc input
srcDir = os.path.abspath(os.path.join(siteFeatures, "../.."))


#Check to see if target directory exists.  If not, create it.
if not os.path.exists(targetDir):
    os.makedirs(targetDir)
    print "Created", targetDir


#read the Sitename from each point in the site feature class

with arcpy.da.SearchCursor(siteFeatures,
                           ("facility_name","fulcrum_id")) as cursor:

    #create a dictionary to link fulcrum_id to directory.
    #This will allow linkage between image and directory later on.
    parents = {}

    #iterate through the site feature class
    for site in cursor:

        #create directories for each site in targetDir
        siteDir = targetDir + site[0]
        pdfDir = siteDir + "/Reports/"
        imgDir = siteDir + "/Images/"
        if not os.path.exists(siteDir):
            os.mkdir(siteDir)
            print "Created", siteDir
            if not os.path.exists(pdfDir):
                os.mkdir(pdfDir)
                print "Created", pdfDir
            if not os.path.exists(imgDir):
                os.mkdir(imgDir)
                print "Created", imgDir

        #Copy the pdfs to the new directories.

        srcPDF = os.path.join(srcDir, site[1] + ".pdf")
        print "Source PDF:", srcPDF
        dstPDF = os.path.join(pdfDir, site[0] + ".pdf")
        print "Destination PDF:", dstPDF
        shutil.copy(srcPDF, dstPDF)

        #Link each site's fulcrum_id to its image directory in a dictionary.
        
        parents[site[1]] = imgDir


#Use a cursor to find to look at the image names.

with arcpy.da.SearchCursor(wtFeatures,
                           ("photos","fulcrum_parent_id","wt_date")) as cursor2:

    for wt in cursor2:
        

        #Split the 'photos' field at commas to get the photo filenames
        photolist = wt[0].split(",")

        

        #Reset count for renaming images for each walkthrough.
        count = 0

        #For each photo in the filename in the list,
        #create a source and destination filepath.

        for photo in photolist:
            if photo is not None:
                count =  count + 1
                
                srcImg = os.path.join(srcDir, photo + ".jpg")
                print "Source image:", srcImg
                
                dstImg = os.path.join(parents[wt[1]], "Fulcrum " +
                                      wt[2] + "_img" + str("%03d" % count) + ".jpg")
                
                print "Destination image:", dstImg

                #execute copy
                shutil.copy(srcImg, dstImg)

