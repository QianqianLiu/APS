% Plot ocean HYCOM node values for sensitivity experiments  

clear all
load Obc_SLR_2098-2019_ssp370.txt
load Obc_SLR_2098-2019_SSP585.txt

obc_ssp370_ann=mean(Obc_SLR_2098_2019_ssp370,2);
obc_ssp585_ann=mean(Obc_SLR_2098_2019_SSP585,2);

close all
figure
plot(obc_ssp585_ann,'r')
hold on
plot(obc_ssp370_ann,'b')
% hold on
% plot(2002,'g') % need to find 2002 hycom data
title('CMIP6 Scenario MSL')
legend({'SSP 585', 'SSP 370','2002'}, 'Location', 'north')
xlabel('Node')
xlim([0 205])
ylabel('Mean Sea Level (m)')
grid on
hold off

saveas(gcf, 'CMIP6_MSL_nodes.png')
