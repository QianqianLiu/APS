
# Total drainage area of Tar-Pamlico River: 3220

#setwd( "/home/liuq/SFlounder/Rivs/")
setwd( "/Users/kboothomefolder/SFlounder/Rivs/")

# Modify date and calculate discharge for available datasets 1978 - 2021
# convert discharge from cubic feet per second (cfs) to cubic meters per second (cms)


data <- read.table("TarAtGreenvile.txt",header = FALSE, sep = "", quote = "\"'", skip = 32)
colnames(data) <- c("Org","Site","Date","HrMn","c1","discharge","c2")
data$Time <- strptime(paste(as.character(data$Date),as.character(data$HrMn)),format="%Y-%m-%d %H:%M")
data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()
data$Discharge <- data$discharge*0.0283168
tar_greenvile <- data

data <- read.table("TarAtRockyM.txt",header = FALSE, sep = "", quote = "\"'", skip = 34)
colnames(data) <- c("Org","Site","Date","c1","c2","c3","c4","discharge","c5")
data$Time <- strptime(as.character(data$Date),format="%Y-%m-%d")
data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()
data$Discharge <- as.numeric(data$discharge)*0.0283168
tar_rockym <- data

# drainage area: 2183
data <- read.table("TarAtTarboro.txt",header = FALSE, sep = "", quote = "\"'", skip = 34)
colnames(data) <- c("Org","Site","Date","c1","c2","c3","c4","discharge","c5")
data$Time <- strptime(as.character(data$Date),format="%Y-%m-%d")
data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()
data$Discharge <- as.numeric(data$discharge)*0.0283168
tar_tarboro <- data

data <- read.table("PamlicoAtWashington.txt",header = FALSE, sep = "", quote = "\"'", skip = 32)
colnames(data) <- c("Org","Site","Date","c1","c2","c3","c4","discharge","c5")
data$Time <- strptime(as.character(data$Date),format="%Y-%m-%d")
data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()
data$Discharge <- data$discharge*0.0283168
pamlico_washington <- data

data <- read.table("Neuse_Kingston.txt",header = FALSE, sep = "", quote = "\"'", skip = 32)
colnames(data) <- c("Org","Site","Date","c1","c2","c3","c4","discharge","c5")
data$Time <- strptime(as.character(data$Date),format="%Y-%m-%d")
data$TimeGMT <- data$Time+4*3600 ## from EDT to GMT ()
data$discharge <- suppressWarnings(as.numeric(as.character(data$discharge))) # replace non-numeric with NA
data$Discharge <- data$discharge*0.0283168
neuse_kingston <- data

# Check for numeric values in discharge array
#discharge_numeric <- as.numeric(as.character(data$discharge))
#non_numeric_values <- is.na(discharge_numeric)
#num_non_numeric_values <- sum(non_numeric_values)
#num_non_numeric_values
# data$discharge <- suppressWarnings(as.numeric(as.character(data$discharge))) # replace non-numeric with NA



########################### Time Series Pamlico Sound Discharge ##############

# Plot two datasets used for riv.ann in GAM
png(filename = "PS_discharge.png", width = 800, height = 600)
plot(tar_tarboro$Time, tar_tarboro$Discharge, 
     xlim = c(ISOdate(1978, 1, 1), ISOdate(2021, 1, 1)), 
     type = 'l', col = 'green', 
     xlab = 'Time', 
     ylab = expression('Discharge (' * m^3 * '/s)'), 
     main = 'River Discharge 1978 - 2021')
lines(neuse_kingston$TimeGMT, neuse_kingston$Discharge, col = 'blue')
legend('topleft', 
       legend = c('Tar at Tarboro', 'Neuse at Kingston'), 
       col = c('green', 'blue'), 
       lty = 1, 
       bty = 'n',
       cex=0.5)
dev.off()

# Plot two datasets used for riv.ann in GAM
png(filename = "PS_discharge_2019.png", width = 800, height = 600)
plot(tar_tarboro$Time, tar_tarboro$Discharge, 
     xlim = c(ISOdate(2019, 1, 1), ISOdate(2020, 1, 1)), 
     type = 'l', col = 'green', 
     xlab = 'Time', 
     ylab = expression('Discharge (' * m^3 * '/s)'), 
     main = 'River Discharge 2019')
lines(neuse_kingston$TimeGMT, neuse_kingston$Discharge, col = 'blue')
legend('topleft', 
       legend = c('Tar at Tarboro', 'Neuse at Kingston'), 
       col = c('green', 'blue'), 
       lty = 1, 
       bty = 'n',
       cex=0.5)
dev.off()

# Add the lines for the other datasets - make sure to update the legend!
#lines(tar_rockym$TimeGMT, tar_rockym$Discharge, col = 'purple')
#lines(tar_greenvile$TimeGMT, tar_greenvile$Discharge, col = 'black')
#lines(pamlico_washington$TimeGMT, pamlico_washington$Discharge, col = 'red')


####################### Plot Monthly Mean Discharge for both stations #######3

# Load required libraries
library(dplyr)
library(ggplot2)
library(lubridate)

# Calculate monthly mean discharge for Tarboro station
tarboro_monthly_mean <- tar_tarboro %>%
  mutate(Month = month(Time)) %>%
  group_by(Month) %>%
  summarize(MonthlyMeanDischarge = mean(Discharge, na.rm = TRUE))

# Calculate monthly mean discharge for Kingston station
kingston_monthly_mean <- neuse_kingston %>%
  mutate(Month = month(TimeGMT)) %>%
  group_by(Month) %>%
  summarize(MonthlyMeanDischarge = mean(Discharge, na.rm = TRUE))

# Combine both datasets for plotting
combined_data <- bind_rows(
  tarboro_monthly_mean %>% mutate(Station = "Tar at Tarboro"),
  kingston_monthly_mean %>% mutate(Station = "Neuse at Kingston")
)

# Plot the data using ggplot2
ggplot(combined_data, aes(x = Month, y = MonthlyMeanDischarge, color = Station)) +
  geom_point() +  
  geom_line() +   
  scale_x_continuous(breaks = 1:12, labels = month.name) +  # Label x-axis with month names
  labs(title = "Average Monthly Discharge (1978-2021)",
       x = "Month",
       y = expression('Discharge (' * m^3 * '/s)')) +
  theme_minimal() +
  scale_color_manual(values = c("green", "blue")) +
  theme(
    legend.title = element_blank(),
    axis.text.x = element_text(angle = 45, hjust = 1),  # Rotate x-axis labels
    legend.position = c(0.95, 0.95),  # Position legend inside the plot area (top right)
    legend.justification = c("right", "top"),  # Adjust legend alignment
    plot.title = element_text(hjust = 0.5),  # Center the title
    panel.grid.major = element_blank(),  # Remove major grid lines
    #panel.grid.minor = element_blank()   # Remove minor grid lines
  )

ggsave("monthly_average_discharge.png", width = 10, height = 6)

# monthly plot for Pasquotank, Roanoke, Tar, Neuse, New, Cape Fear, Black
