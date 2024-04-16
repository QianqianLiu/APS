function h1=colorbar_hori_rb(pos,cmin,cmax,step,xlab,ln,cc);
%Used to be:colorbar_hori_rb(pos,cmin,cmax,step,xlab,ln,cc1,cc2);
%colorbar_hori_rb(pos,cmin,cmax,step,xlab,ln,cc)
%colorbar_hori_rb(pos,cmin,cmax,step,xlab,ln)
%pos: position of colorbar
%cmin: minimum value
%cmax: maximum value
%step: step for the colorbar
%ylabel: label for the colorbar
%ln: step*ln is the step for the colorbar label 
%b: the begin color
%m: the middle color
%e: the end color
%cc=[cc1;cc2] is the self defined colormap
 % for example
 % 1. apply jet colormap to the values smaller than 0
 % cc1=jet(length([cmin:step:cmax])); m=cc1(end,:); e=(1,0,0);
 % for i=1:3; cc2(:,i)=linspace(m(:,i),e(:,i),length([0:step:cmax])));
 % cc=[cc1(1:end-1,:);cc2(1:end-1,:)];
 % 2. apply jet colormap to the values larger than 0
 % cc2=jet(length(0:step:cmax)); m=cc2(1,:); b=(0,0,1);
 % for i=1:3; cc1(:,i)=linspac(b(:,i),m(:,i),length([cmin:step:0]));
 % cc=[cc1(1:end-1,:);cc2(1:end-1,:)];
%%%A or B should be jet colormap
%%%If A is jet colormap, B is end color, otherwise,
%%%B is jet colormap, A is begin color.
%%%-----------By Qianqian Liu, GSO, URI, Jan 2013 ------------

 L1=length([cmin:step:0]);
 L2=length([0:step:cmax]);

switch nargin
 case 6
 e=[1,0,0]; %reb
 m=[.9,.9,.9]; %middle
 b=[0,0,1]; %blue
 c1=zeros(L1,3); c2=zeros(L2,3);
   for i=1:3;
   c1(:,i)=linspace(b(i),m(i),L1);
   c2(:,i)=linspace(m(i),e(i),L2);
   end
   c=[c1(1:end-1,:);c2(1:end-1,:)];
   maplength=L1+L2-2;
 otherwise
 c=cc; %c=[cc1(1:end-1,:);cc2(1:end-1,:)];
 [maplength,aa]=size(c);
end

caxis([cmin cmax])
colormap(c)
hold on

if ~isempty(pos)
axes('Position',pos)
for k=1:maplength
x1=cmin+(k-1)*step; x2=x1+step;
fill(   [ x1 x1 x2 x2 ],[0 0.7 0.7 0], c(k,:) );hold on
end
axis([cmin cmax 0 0.7])
xlabel(xlab, 'VerticalAlignment', 'top','fontsize',10,'fontweight','bold' )
xtick=[cmin:step*ln:cmax];labels=num2str(xtick');
% Set up first set of axes, label them
h1 = gca;
set(h1,'YAxisLocation', 'right','fontweight','bold' )
set(h1,'XAxisLocation', 'bottom','fontweight','bold' )
set(h1,'ytick', []);
set(h1,'XTICK',xtick,'XTICKLABEL',labels,'fontsize',10)%,'fontweight','bold');
end

