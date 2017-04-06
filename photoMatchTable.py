import arcpy, os

inputFeatures = arcpy.GetParameterAsText(0)
photofield = arcpy.GetParameterAsText(1)
picfolder = arcpy.GetParameterAsText(2)
matchTable = arcpy.GetParameterAsText(3)


#create table in gdb

arcpy.CreateTable_management(*os.path.split(matchTable))

#add fields to table

field1 = "MatchID"
field1length = 5
field2 = "path"
field2length = 100

arcpy.AddField_management(matchTable, field1, "SHORT", field_length=field1length)
arcpy.AddField_management(matchTable, field2, "TEXT", field_length=field2length)


#create insert cursor to update match table

InsC = arcpy.da.InsertCursor(matchTable, ("MatchID","path"))

#create search cursor to read feature class attributes

cursor = arcpy.da.SearchCursor(inputFeatures, ("OBJECTID",photofield))

#use the search cursor to iterate over the feature class

featuresCount = 0
photosCount = 0

for row in cursor:
    if row[1] is not None:
        featuresCount = featuresCount + 1
        #split the photo names strings at commas
        photolist = row[1].split(",")
    
        #for each item in the above created list, define a new row as (objectid, 'folder/imagename.jpg').
        #then, write the row to the match table using the InsertCursor object.
        for photo in photolist:
            photosCount = photosCount + 1
            R = (row[0], picfolder + '\\' + photo + '.jpg')
            InsC.insertRow(R)


arcpy.AddMessage('Match table created with ' + str(photosCount) + ' photos matched to ' + str(featuresCount) + ' features.')
        
