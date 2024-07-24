
setwd( "/Users/kboothomefolder/git_liu/APS/usgs/")
rm(list = ls())

# Modify date and calculate discharge for available datasets 1978 - 2021
# convert discharge from cubic feet per second (cfs) to cubic meters per second (cms)

#Pasquotank   -- source_sink.in;  usgs station: 0204382800 - Pasquotank River near South Mills
#Roanoke -- 2; usgs station: 02080500 - Roanoke River at Roanoke Rapids
#Tar (Pamico River) -- 3; usgs station: 02084000 - Tar River at Greenville
#Neuse -- 4; usgs station: 02091814 - Neuse River at Fort Barnwell
#New -- source in source_sink.in; usgs station: 02093000 - New River near Gum Branch
#Cape Fear -- 5; usgs station: 02105769 (Cape Fear R at Lock #1 NR Kelly NC) and USGS 02106500 BLACK RIVER NEAR TOMAHAWK, NC

#############################################################################

library(dplyr)

calc_month_discharge <- function(file_path) {
  data <- read.table(file_path,
                     header = TRUE,  # Use the first row as column names
                     sep = "\t",     # Assuming columns are tab-separated
                     skip = 27,       # Skip lines of metadata and heading lines
                     stringsAsFactors = FALSE)  # Prevent conversion of strings to factors
  
  colnames(data) <- c("USGS", "sta_no", "Time", "Timezone", "Discharge", "A")
  
  data$Time <- strptime(as.character(data$Time), format="%Y-%m-%d %H:%M")
  data$Discharge <- data$Discharge * 0.0283168
  data$Date <- as.Date(data$Time)
  
  daily_mean_discharge <- data %>%
    group_by(Date) %>%
    summarize(DailyMeanDischarge = mean(Discharge, na.rm = TRUE))
  return(daily_mean_discharge)
}

directory <- "/Users/kboothomefolder/git_liu/APS/usgs/"

files <- c("Neuse_02091814_2017_2019_15min.txt",
           "Tar_02084000_2017_2019_15min.txt",
           "Roanoke_02080500_2017_2019_15min.txt",
           "Pasquotank_0204382800_2017_2019_15min.txt",
           "New_02093000_2017_2019_15min.txt",
           "CapeFear_02105769_2017_2019_15min.txt")

file_paths <- file.path(directory, files)
discharge_2019 <- lapply(file_paths, calc_month_discharge)
names(discharge_2019) <- c("Neuse_Kingston", "Tar_Greenville", "Roanoke_Rapids","Pasquotank", "New", "Cape_Fear")

# Filter datasets for the year 2019
filter_2019 <- function(data) {
  data %>% filter(Date >= as.Date("2019-01-01") & Date < as.Date("2020-01-01"))
}

neuse_kingston <- filter_2019(discharge_2019[[1]])
tar_greenville <- filter_2019(discharge_2019[[2]])
roanoke_rapids <- filter_2019(discharge_2019[[3]])
pasquotank <- filter_2019(discharge_2019[[4]])
new <- filter_2019(discharge_2019[[5]])
cape_fear <- filter_2019(discharge_2019[[6]])

########################### Time Series Pamlico Sound Discharge ##############
     

png(filename = "discharge_2019.png", width = 1200, height = 800)
par(mfrow = c(3, 1))  # 3 rows, 1 column

# Subplot 1: Tar at Greenville and Neuse at Kingston
plot(tar_greenville$Date, tar_greenville$DailyMeanDischarge, 
     type = 'l', 
     col = 'green',
     ylab = expression('Discharge (' * m^3 * '/s)'), 
     main = 'Tar at Greenville and Neuse at Kingston')
lines(neuse_kingston$Date, neuse_kingston$DailyMeanDischarge, col = 'blue')
legend('topright', 
       legend = c('Tar at Greenville', 'Neuse at Kingston'), 
       col = c('green', 'blue'), 
       lty = 1, 
       bty = 'n',
       cex=0.9)

# Subplot 2: Roanoke Rapids and Pasquotank
plot(pasquotank$Date, pasquotank$DailyMeanDischarge, 
     type = 'l', 
     col = 'red', 
     ylab = expression('Discharge (' * m^3 * '/s)'), 
     main = 'New and Pasquotank')
lines(new$Date, new$DailyMeanDischarge, col = 'purple')
legend('topright', 
       legend = c('Pasquotank', 'New'), 
       col = c('red', 'purple'), 
       lty = 1, 
       bty = 'n',
       cex=0.9)

# Subplot 3: New and Cape Fear
plot(roanoke_rapids$Date, roanoke_rapids$DailyMeanDischarge, 
     type = 'l', 
     col = 'orange', 
     xlab = 'Time', 
     ylab = expression('Discharge (' * m^3 * '/s)'), 
     main = 'Roanoke and Cape Fear')
lines(cape_fear$Date, cape_fear$DailyMeanDischarge, col = 'brown')
legend('topright', 
       legend = c('Roanoke', 'Cape Fear'), 
       col = c('orange', 'brown'), 
       lty = 1, 
       bty = 'n',
       cex=0.9)

dev.off()

