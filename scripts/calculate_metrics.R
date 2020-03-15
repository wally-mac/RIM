#############################
#set local directory and inputs
#############################

#set local working directory:
localdir <- "C:\\Users\\a02295870\\Box\\0_ET_AL\\NonProject\\etal_Drone\\2019\\Inundation_sites\\"

sitename <- "kane_creek"

#folder with the data
datapath <- paste(localdir, "Idaho\\kane_creek\\20190913\\GIS", sep="\\") 


#folder for output summary data
outputpath <- paste(datapath, "stats", sep="\\")

##folder containing any neccessary scripts to link to

#Scriptpath <- 

#library dependencies: 
library(sp)
library(dplyr)
library(sf)
library(rgdal)
library(rgeos)
library(rmapshaper)
library(raster)
#install.packages("ggplot2", dependencies = T)
library(ggplot2)

#set paths for input shapefiles
valleybottompath <- paste(datapath,"valley_bottom.shp", sep="\\") 
damcrestspath <- paste(datapath,"dam_crests.shp", sep="\\") 
inundationpath <- paste(datapath,"inundation.shp", sep="\\")
inundationpath_pre <- paste(datapath,"inundation_pre.shp", sep="\\")
VBcenterlinepath <- paste(datapath, "vb_centerline.shp", sep="\\")
BRATpath <- paste(datapath, "BRAT.shp", sep="\\")
thalwegpath <- paste(datapath, "thalwegs.shp", sep="\\")
activechpath <- paste(datapath, "active_channel.shp", sep="\\")
activechpath_pre <- paste(datapath, "active_channel_pre.shp", sep="\\")

######other inputs

#is the site active?
active<-"yes"

#is the site maintained>
maintained="yes"

#what is the site bankfull width if there were no beaver dams?
bfw <- as.numeric("10")

#what is the cluer and thorne stage?
CT_stage <- 0

#reads in the shapefile inputs
valleybottom <- readOGR(dsn=valleybottompath)
damcrests <- readOGR(damcrestspath)
inundation <- readOGR(inundationpath)
inundation_pre <- readOGR(inundationpath_pre)
VBcenterline <- readOGR(VBcenterlinepath)
BRAT <- readOGR(BRATpath)
thalweg <- readOGR(thalwegpath)
activech <- readOGR(activechpath)
activech_pre <- readOGR(activechpath_pre)

#add area and length calculations
valleybottom$area <- area(valleybottom)
damcrests$crest_len <- gLength(damcrests, byid = TRUE)
inundation$area <- area(inundation)
inundation_pre$area <- area(inundation_pre)
inundation$perim <- gLength(inundation, byid = TRUE)
inundation_pre$perim <- gLength(inundation_pre, byid = TRUE)
thalweg$length <- gLength(thalweg, byid = TRUE)
VBcenterline$length <- gLength(VBcenterline, byid = TRUE)
activech$area <- area(activech)
activech_pre$area <- area(activech_pre)

# #write the shapefile objects to a csv
write.csv(valleybottom, file=paste(datapath, "valley_bottom.csv", sep="\\"))
write.csv(damcrests, file=paste(datapath,"damcrests.csv", sep="\\"))
write.csv(inundation, file=paste(datapath,"inundation.csv", sep="\\"))
write.csv(inundation_pre, file=paste(datapath,"inundation_pre.csv", sep="\\"))
write.csv(VBcenterline, file=paste(datapath,"VBcenterline.csv", sep="\\"))
write.csv(BRAT, file=paste(datapath,"BRAT.csv", sep="\\"))
write.csv(thalweg, file=paste(datapath,"thalweg.csv", sep="\\"))
write.csv(activech, file=paste(datapath,"activech.csv", sep="\\"))
write.csv(activech_pre, file=paste(datapath,"activech_pre.csv", sep="\\"))

# #read in csv
valleybottom <- read.csv(paste(datapath,"valley_bottom.csv", sep="\\"))
damcrests <- read.csv(paste(datapath,"damcrests.csv", sep="\\"))
inundation <- read.csv(paste(datapath,"inundation.csv", sep="\\"))
inundation_pre <- read.csv(paste(datapath,"inundation_pre.csv", sep="\\"))
VBcenterline <- read.csv(paste(datapath,"VBcenterline.csv", sep="\\"))
BRAT <- read.csv(paste(datapath,"BRAT.csv", sep="\\"))
thalweg <- read.csv(paste(datapath,"thalweg.csv", sep="\\"))
activech <- read.csv(paste(datapath,"activech.csv", sep="\\"))
activech_pre <- read.csv(paste(datapath,"activech_pre.csv", sep="\\"))

###############
#calculate site metrics
###############

#add valley length
valleybottom$valley_len=VBcenterline$length

##calculate valley width
valleybottom$valley_wid=valleybottom$area/valleybottom$valley_len

#add thalweg length
#valleybottom$thalweg_len=thalweg$length

#calculate sinuosity
#valleybottom$sin=valleybottom$thalweg_len/valleybottom$valley_len

###add metrics from BRAT

# #add stream name
# valleybottom$stream=BRAT$StreamName

#add gradient
valleybottom$grad=BRAT$iGeo_Slope

# #add upstream drainage area
# valleybottom$DA=BRAT$iGeoDA

#add Q2
valleybottom$Q2=BRAT$iHyd_Q2

#add Qlow
valleybottom$Qlow=BRAT$iHyd_QLow

#add high and low flow stream power
valleybottom$SP2=BRAT$iHyd_SP2
valleybottom$SPLow=BRAT$iHyd_SPLow

#add bfw
valleybottom$bfw=bfw

#make a VB objet for pre beaver metrics
valleybottom_pre <- valleybottom

###############
#calculate inundation metrics
###############

###calculate areas for each inundation type

#calculate total area of all inundation types
valleybottom$total_inun=sum(inundation$area)

#calculate total area of free flowing inundation
valleybottom$total_FF=sum(inundation$area[inundation$type=="free_flowing"])

#calculate total area of ponded inundation
valleybottom$total_ponded=sum(inundation$area[inundation$type=="ponded"])

#calculate total area of overflow inundation
valleybottom$total_OV=sum(inundation$area[inundation$type=="overflow"])

###calculate perimeters
#calculate total perimeter of all inundation types
valleybottom$perimeter_all=sum(inundation$perimeter)

#calculate total perimeter of free flowing inundation
valleybottom$perimeter_FF=sum(inundation$perimeter[inundation$type=="free_flowing"])

#calculate total perimeter of ponded inundation
valleybottom$perimeter_ponded=sum(inundation$perimeter[inundation$type=="ponded"])

#calculate total area of overflow inundation
valleybottom$perimeter_OV=sum(inundation$perimeter[inundation$type=="overflow"])

###calculate percents
#calculate proportion of all inundation types
valleybottom$percent_inun=valleybottom$total_inun/valleybottom$area * 100

#calculate proportion of free flowing inundation
valleybottom$percent_FF=valleybottom$total_FF/valleybottom$area * 100

#calculate proportion of ponded inundation
valleybottom$percent_ponded=valleybottom$total_ponded/valleybottom$area * 100

#calculate proportion of overflow inundation
valleybottom$percent_OV=valleybottom$total_OV/valleybottom$area * 100

# percent dry
valleybottom$percent_dry <- 100 - valleybottom$percent_inun

# active channel area and percent of valley bottom
valleybottom$ActCh_area <- activech$area

valleybottom$percent_actCh <- valleybottom$ActCh_area/valleybottom$area * 100




###calculate perimeter:area ratio

#calculate perimeter:area for all inundation types
valleybottom$ratio_PA=valleybottom$perimeter_all/valleybottom$total_inun

#calculate perimeter:area for free flowing 
valleybottom$ratio_PA_FF=valleybottom$perimeter_FF/valleybottom$total_FF

#calculate perimeter:area for overflow inundation types
valleybottom$ratio_PA_OV=valleybottom$perimeter_OV/valleybottom$total_OV

#calculate perimeter:area for ponded inundation types
valleybottom$ratio_PA_ponded=valleybottom$perimeter_ponded/valleybottom$total_ponded

#################
#generate other variables
#################

#calculate total # of dams
valleybottom$damcount=length(damcrests$Id)

#add dam density
valleybottom$dam_density=valleybottom$damcount/(valleybottom$valley_len/1000)

#calculate dam state info
#calculate number intact, breached, blown-out
valleybottom$num_intact=nrow(damcrests[damcrests$dam_state == "intact",])
valleybottom$num_breached=nrow(damcrests[damcrests$dam_state == "breached",])
valleybottom$num_blownout=nrow(damcrests[damcrests$dam_state == "blown-out",])

#calculate length of intact, breached, blown out dams / valley length
valleybottom$crestlen_valleylen=sum(damcrests$crest_len)/valleybottom$valley_len
valleybottom$crestlen_valleylen_intact=sum(damcrests$crest_len[damcrests$dam_state == "intact"])/valleybottom$valley_len
valleybottom$crestlen_valleylen_breached=sum(damcrests$crest_len[damcrests$dam_state == "breached"])/valleybottom$valley_len
valleybottom$crestlen_valleylen_blownout=sum(damcrests$crest_len[damcrests$dam_state == "blown-out"])/valleybottom$valley_len

#calculate proportion of dams that are intact, breached, blown-out
valleybottom$proportion_intact=valleybottom$num_intact/valleybottom$damcount
valleybottom$proportion_breached=valleybottom$num_breached/valleybottom$damcount
valleybottom$proportion_blownout=valleybottom$num_blownout/valleybottom$damcount

#calculate dam crest to bfw ratio
damcrests$crestlen_bfw=damcrests$crest_len/bfw
valleybottom$mean_crestlen_bfw=mean(damcrests$crestlen_bfw)
valleybottom$med_crestlen_bfw=median(damcrests$crestlen_bfw)

#is maintained?
valleybottom$maintained=maintained

#is active?
valleybottom$active=active

#cluer and thorne stage
valleybottom$ct_stage=CT_stage

#calculate integrated wetted width
valleybottom$ww <- (valleybottom$total_inun/valleybottom$valley_len)

#stream power integrated ww ratio
valleybottom$spLow_ww <- (valleybottom$SPLow/valleybottom$ww)

valleybottom$sp2_ww <- (valleybottom$SP2/valleybottom$ww)

##############################################
#calculate pre beaver inundation metrics
##############################################
###############
#calculate inundation_pre metrics
###############

###calculate areas

#calculate total area of all inundation_pre types
valleybottom_pre$total_inun=sum(inundation_pre$area)

#calculate total area of free flowing inundation_pre
valleybottom_pre$total_FF=sum(inundation_pre$area[inundation_pre$type=="free_flowing"])

#calculate total area of ponded inundation_pre
valleybottom_pre$total_ponded=sum(inundation_pre$area[inundation_pre$type=="ponded"])

#calculate total area of overflow inundation_pre
valleybottom_pre$total_OV=sum(inundation_pre$area[inundation_pre$type=="overflow"])

###calculate perimeters
#calculate total perimeter of all inundation_pre types
valleybottom_pre$perimeter_all=sum(inundation_pre$perimeter)

#calculate total perimeter of free flowing inundation_pre
valleybottom_pre$perimeter_FF=sum(inundation_pre$perimeter[inundation_pre$type=="free_flowing"])

#calculate total perimeter of ponded inundation_pre
valleybottom_pre$perimeter_ponded=sum(inundation_pre$perimeter[inundation_pre$type=="ponded"])

#calculate total area of overflow inundation_pre
valleybottom_pre$perimeter_OV=sum(inundation_pre$perimeter[inundation_pre$type=="overflow"])

###calculate percents
#calculate proportion of all inundation_pre types
valleybottom_pre$percent_inun=valleybottom_pre$total_inun/valleybottom_pre$area * 100

#calculate proportion of free flowing inundation_pre
valleybottom_pre$percent_FF=valleybottom_pre$total_FF/valleybottom_pre$area * 100

#calculate proportion of ponded inundation_pre
valleybottom_pre$percent_ponded=valleybottom_pre$total_ponded/valleybottom_pre$area * 100

#calculate proportion of overflow inundation_pre
valleybottom_pre$percent_OV=valleybottom_pre$total_OV/valleybottom_pre$area * 100

# percent dry
valleybottom_pre$percent_dry <- 100 - valleybottom_pre$percent_inun

###calculate perimeter:area ratio

#calculate perimeter:area for all inundation_pre types
valleybottom_pre$ratio_PA=valleybottom_pre$perimeter_all/valleybottom_pre$total_inun

#calculate perimeter:area for free flowing 
valleybottom_pre$ratio_PA_FF=valleybottom_pre$perimeter_FF/valleybottom_pre$total_FF

#calculate perimeter:area for overflow inundation_pre types
valleybottom_pre$ratio_PA_OV=valleybottom_pre$perimeter_OV/valleybottom_pre$total_OV

#calculate perimeter:area for ponded inundation_pre types
valleybottom_pre$ratio_PA_ponded=valleybottom_pre$perimeter_ponded/valleybottom_pre$total_ponded

#active channel area and percentage of valley bottom for pre beaver
valleybottom_pre$ActCh_area <- activech_pre$area

valleybottom_pre$percent_actCh <- valleybottom_pre$ActCh_area/valleybottom_pre$area * 100
#################
#generate other variables
#################

#calculate total # of dams
valleybottom_pre$damcount <- 0

#add dam density
valleybottom_pre$dam_density=valleybottom_pre$damcount/(valleybottom_pre$valley_len/1000)

#calculate dam state info
#calculate number intact, breached, blown-out
valleybottom_pre$num_intact=0
valleybottom_pre$num_breached=0
valleybottom_pre$num_blownout=0

#calculate length of intact, breached, blown out dams / valley length
valleybottom_pre$crestlen_valleylen=0
valleybottom_pre$crestlen_valleylen_intact=0
valleybottom_pre$crestlen_valleylen_breached=0
valleybottom_pre$crestlen_valleylen_blownout=0

#calculate proportion of dams that are intact, breached, blown-out
valleybottom_pre$proportion_intact=0
valleybottom_pre$proportion_breached=0
valleybottom_pre$proportion_blownout=0

#calculate dam crest to bfw ratio
damcrests$crestlen_bfw=0
valleybottom_pre$mean_crestlen_bfw=0
valleybottom_pre$med_crestlen_bfw=0

#is maintained?
valleybottom_pre$maintained=maintained

#is active?
valleybottom_pre$active=active

#cluer and thorne stage
valleybottom_pre$ct_stage=CT_stage

#calculate integrated wetted width
valleybottom_pre$ww <- (valleybottom_pre$total_inun/valleybottom_pre$valley_len)

#stream power integrated ww ratio
valleybottom_pre$spLow_ww <- (valleybottom_pre$SPLow/valleybottom_pre$ww)

valleybottom_pre$sp2_ww <- (valleybottom_pre$SP2/valleybottom_pre$ww)

############################################
#combine pre and post
############################################
summary <- rbind(valleybottom_pre, valleybottom)
summary$X <- sitename
summary$visit <- "pre"
summary$visit[2] <- "post"

###############
#write output to csv
###############

#write the shapefile objects to a csv
write.csv(summary, file=paste(outputpath, "summary.csv", sep="\\"))


##################
#plots
##################

#manipulate data for plotting
visit <- c(rep("pre", 3), rep("post", 3))
type <- rep(c("Free flowing", "Ponded", "Overflow"), 2)
percent <- c(summary$percent_FF[which(summary$visit == "pre")], summary$percent_ponded[which(summary$visit == "pre")],
             summary$percent_OV[which(summary$visit == "pre")], summary$percent_FF[which(summary$visit == "post")], 
             summary$percent_ponded[which(summary$visit == "post")], summary$percent_OV[which(summary$visit == "post")])

percentInun <- data.frame(visit, type, percent)

#bar plot of pre and post beaver inundation
bp <- ggplot(percentInun, aes(x=visit, y=percent, fill=type)) + geom_bar(position = position_stack(reverse = TRUE), stat="identity") + ylim(0, 100)

ggsave(filename = "barplot.pdf", path = outputpath)

#pie chart of inundation pre and post beaver
## pre
inunPre <- percentInun[visit == "pre",]
bpPre <- ggplot(inunPre, aes(x="", y=percent, fill=type)) + geom_bar(position="stack", stat="identity")

piePre <- bpPre + coord_polar("y")

piePre + theme(axis.text.x=element_blank(), axis.ticks=element_blank(), panel.grid  = element_blank()) + xlab("") + ylab("")

ggsave(filename = "piePre.pdf", path = outputpath)

## post
inunPost <- percentInun[visit == "post",]
bpPost <- ggplot(inunPost, aes(x="", y=percent, fill=type)) + geom_bar(position="stack", stat="identity")

piePost <- bpPost + coord_polar("y")

piePost + theme(axis.text.x=element_blank(), axis.ticks=element_blank(), panel.grid  = element_blank()) + xlab("") + ylab("")

ggsave(filename = "piePost.pdf", path = outputpath)

bph <- ggplot(percentInun, aes(x=visit, y=percent, fill=type)) + geom_bar(position = position_stack(reverse = TRUE), stat="identity") + ylim(0, 100) + coord_flip()

ggsave(filename = "barplot_horz.pdf", path = outputpath)

###### 
#plot active channel
#####
# summary %>%
#   ggplot(aes(visit, percent_actCh)) +
#   geom_boxplot()
# 
#  dev.off()

#############################
#add summary data to spreadsheet with all site data
# 
other_sites <- read.csv(paste(localdir, "all\\Rscripts\\site_data.csv", sep="\\"))

all_sites <- bind_rows(other_sites, summary)

write.csv(all_sites, file = paste(localdir, "all\\Rscripts\\site_data.csv", sep="\\"))
