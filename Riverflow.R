setwd('~/Documents/Research/NorthCarolinaCoastal/pylibs/Scripts/')

data0 <- strptime("2019-01-01 00:00",format="%Y-%m-%d %H:%M")

require(readxl)
# Chowan River discharge
flow <- read_excel("ChowanFlow_2013_27Apr2021.xlsx",1) #
flow$time <- as.POSIXct(flow$date*3600*24,origin = "1900-01-01",tz = "GMT")
flow$discharge <- flow$`Interpolate Chowan flow (CFS)` *0.0283168 # convert unit to cms
flow$jday <- as.numeric(difftime(flow$time,data0,units = "days"))+0.2083333 
## why 2019,1,1 is not 0? I correct it to 0 to make up for the difference. There might be potential problem with this...
data_Chowan <- flow[flow$jday>-0.001,]


# Pasquotank River
data <- read.table("Pasquotank_2019_Discharge.txt",header=FALSE,sep="",quote ="\"'", skip=29)
colnames(data) <- c("Org","Site","Date","HrMn","c1","discharge","c2")
data$Time <- strptime(paste(as.character(data$Date),as.character(data$HrMn)),format="%Y-%m-%d %H:%M")
data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()
data$Discharge_si <- data$discharge*0.0283168
data$Discharge_rescaled <- data$Discharge_si*5630/3900 # rescaled the discharge according to drainage area
data$secs <- difftime(data$Time,data0,units = "secs")
data$jday <- as.numeric(data$secs/3600/24)
data_Pasquotank <- data[data$jday>-0.001,c('jday','Discharge_rescaled')]



# RoanokeRiver
data <- read.table("RoanokeRiver_2019_usgs.txt",header = FALSE, sep = "", quote = "\"'", skip = 32)
colnames(data) <- c("Org","Site","Date","HrMn","c1","discharge","c2","GaugeHeight",
                    "c3")
data$Time <- strptime(paste(as.character(data$Date),as.character(data$HrMn)),format="%Y-%m-%d %H:%M")
data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()

#data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()
data$Discharge <- data$discharge*0.0283168
data$Discharge_rescaled <- data$Discharge*9660/8384 # rescaled the discharge according to drainage area
data$secs <- difftime(data$Time,data0,units = "secs")
data$jday <- as.numeric(data$secs/3600/24)
data_Roanoke <- data[data$jday>-0.001,c('jday','Discharge_rescaled')]


# Tar River
# usgs 02084000 drainage area: 2,660 square miles
# Pamlico River station drainage area: 3,200 square miles
# wiki gives the Pamlico River basin size: 6148 square miles 
# it is missing data before January 12th, 2019. Need to find data for this part
data <- read.table("TarRiver_2019_usgs.txt",header = FALSE, sep = "", quote = "\"'", skip = 32)
colnames(data) <- c("Org","Site","Date","HrMn","c1","discharge","c2")
data$Time <- strptime(paste(as.character(data$Date),as.character(data$HrMn)),format="%Y-%m-%d %H:%M")
data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()
data$Discharge <- data$discharge*0.0283168
data$Discharge_rescaled <- data$Discharge*3200/2660 # rescaled the discharge according to drainage area
data$secs <- difftime(data$Time,data0,units = "secs")
data$jday <- as.numeric(data$secs/3600/24)
data_Pamlico <- data[data$jday>-0.001,c('jday','Discharge_rescaled')]

#Neuse River near Fort Barnwell
# usgs 02091814 drainage area: 3900 square miles
# I estimated the total drainage area as: 3900+370(trent river)+269(SWIFT creek)
# wiki gives the basin size of Neuse River as: 5600 square miles
# DEQ: the basin is more than 6200 square miles
data <- read.table("NeuseRiver_2019_usgs.txt",header = FALSE, sep = "", quote = "\"'", skip = 32)
colnames(data) <- c("Org","Site","Date","HrMn","c1","discharge","c2","Gauge Height","c3")
data$Time <- strptime(paste(as.character(data$Date),as.character(data$HrMn)),format="%Y-%m-%d %H:%M")
data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()
data$Discharge <- data$discharge*0.0283168
data$Discharge_rescaled <- data$Discharge*(3900+370+269)/3900 # rescaled the discharge according to drainage area
data$secs <- difftime(data$Time,data0,units = "secs")
data$jday <- as.numeric(data$secs/3600/24)
data_Neuse <- data[data$jday>-0.001,c('jday','Discharge_rescaled')]

# New River near Gum Branch, NC
# USGS 02093000 drainage area: 94 square miles
# DEQ: give the total area of New River basin in North Carolina is 753 square miles

data <- read.table("NewRiver_usgs_2019.txt",header = FALSE, sep = "", quote = "\"'", skip = 32)
colnames(data) <- c("Org","Site","Date","HrMn","c1","discharge","c2","Gauge Height","c3")
data$Time <- strptime(paste(as.character(data$Date),as.character(data$HrMn)),format="%Y-%m-%d %H:%M")
data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()
data$Discharge <- data$discharge*0.0283168
data$Discharge_rescaled <- data$Discharge # not rescaled for New River
data$secs <- difftime(data$Time,data0,units = "secs")
data$jday <- as.numeric(data$secs/3600/24)
data_New <- data[data$jday>-0.001,c('jday','Discharge_rescaled')]




# Cape Fear River
# including USGS 02105769 CAPE FEAR R AT LOCK #1 NR KELLY, NC and  USGS 02106500 BLACK RIVER NEAR TOMAHAWK, NC
# Should also include the Northeast Cape Fear River, but data for the Northeast Cape Fear is not avaialble

data <- read.table("CapeFearRiver_usgs_2019.txt",header = FALSE, sep = "", quote = "\"'", skip = 32)
colnames(data) <- c("Org","Site","Date","HrMn","TimeZone","discharge","c2")
data$Time <- strptime(paste(as.character(data$Date),as.character(data$HrMn)),format="%Y-%m-%d %H:%M")
data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()
data$Discharge <- data$discharge*0.0283168
data$Discharge_rescaled <- data$Discharge # not rescaled for the Cape Fear River
data$secs <- difftime(data$Time,data0,units = "secs")
data$jday <- as.numeric(data$secs/3600/24)
data_CapeFear1 <- data[data$jday>-0.001,c('jday','Discharge_rescaled')]

data <- read.table("BlackRiver_usgs_2019.txt",header = FALSE, sep = "", quote = "\"'", skip = 32)
colnames(data) <- c("Org","Site","Date","HrMn","TimeZone","discharge","c2")
data$Time <- strptime(paste(as.character(data$Date),as.character(data$HrMn)),format="%Y-%m-%d %H:%M")
data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()
data$Discharge <- data$discharge*0.0283168
data$Discharge_rescaled <- data$Discharge # not rescaled for the Black River
data$secs <- difftime(data$Time,data0,units = "secs")
data$jday <- as.numeric(data$secs/3600/24)
data_Black <- data[data$jday>-0.001,c('jday','Discharge_rescaled')]


# sequence should be: Pasquotank, Chowan, Roanoke, 
Time <- seq(0,365,0.01041667*4) ## dt is one hour 
data_Roanoke_interp <- approx(data_Roanoke$jday, data_Roanoke$Discharge_rescaled,Time)
data_Pasquotank_interp <- approx(data_Pasquotank$jday, data_Pasquotank$Discharge_rescaled,Time)
data_Chowan_interp <- approx(data_Chowan$jday, data_Chowan$discharge,Time)
data_Pamlico_interp <- approx(data_Pamlico$jday, data_Pamlico$Discharge_rescaled,Time)
data_Neuse_interp <- approx(data_Neuse$jday, data_Neuse$Discharge_rescaled,Time)
data_New_interp <- approx(data_New$jday, data_New$Discharge_rescaled,Time)
data_CapeFear1_interp <- approx(data_CapeFear1$jday,data_CapeFear1$Discharge_rescaled,Time)
data_Black_interp <- approx(data_Black$jday,data_Black$Discharge_rescaled,Time)
data_CapeFearRiver <- data.frame(Time=Time,discharge=data_Black_interp$y+data_CapeFear1_interp$y)

write.table(data_CapeFearRiver,file='CapeFearRiver.txt',row.names=FALSE,col.names = FALSE)



plot(data_Roanoke$jday,data_Roanoke$Discharge_rescaled,type='l')
lines(Time,data_Roanoke_interp$y,col='red')
lines(Time,data_Pasquotank_interp$y,col='green')
lines(Time,data_Chowan_interp$y,col='blue')
lines(Time,data_Pamlico_interp$y,col='magenta')
lines(Time,data_Neuse_interp$y,col='cyan')
lines(Time,data_New_interp$y,col='black')
lines(Time,data_CapeFearRiver$discharge,col='black')



#discharge <- data.frame(Time,data_Pasquotank_interp$y,data_Chowan_interp$y,data_Roanoke_interp$y,data_Pamlico_interp$y,
#                        data_Neuse_interp$y,data_New_interp$y)
discharge <- data.frame(Time,data_Chowan_interp$y,data_Roanoke_interp$y,data_Pamlico_interp$y,
                        data_Neuse_interp$y,data_New_interp$y)
discharge$Time <- round(discharge$Time*24*3600)
discharge[,2:6] <- -discharge[,2:6]
# use the first avaiable data for Pamlico River to fill the data before January 12th
discharge$data_Pamlico_interp.y[1:265] <- discharge$data_Pamlico_interp.y[266]
discharge[8761,] <- discharge[8760,]
discharge[8761,1] <- 31536010
write.table(discharge,file='flux_5Rivers.th',row.names=FALSE,col.names = FALSE)

write.table(discharge[,1:5],file='flux_4Rivers.th',row.names=FALSE,col.names = FALSE)

write.table(discharge[,c(1,3,4,5)],file='flux_3Rivers.th',row.names=FALSE,col.names = FALSE)


#### --------- This line is for interpolation......
#discharge <- approx(flow$time,flow$discharge,HabArea2$time)
#write.table(data[,c('jday','Discharge_rescaled')],file="RoanokeRiver_discharge.txt",row.names = FALSE)


# to include the rivers of Chowan, Roanoke, Pamlico, Neuse and Cape Fear
discharge <- data.frame(Time,data_Chowan_interp$y,data_Roanoke_interp$y,data_Pamlico_interp$y,
                        data_Neuse_interp$y,data_CapeFear1_interp$y)

discharge$Time <- round(discharge$Time*24*3600)
discharge[,2:6] <- -discharge[,2:6]
# use the first avaiable data for Pamlico River to fill the data before January 12th
discharge$data_Pamlico_interp.y[1:265] <- discharge$data_Pamlico_interp.y[266]
discharge[8761,] <- discharge[8760,]
discharge[8761,1] <- 31536010
write.table(discharge,file='flux_5Rivers_v2.th',row.names=FALSE,col.names = FALSE)




