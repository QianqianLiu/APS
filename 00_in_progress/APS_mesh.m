fname='./hgrid.gr3';
 
fid=fopen(fname,'r');
char=fgetl(fid);
tmp1=str2num(fgetl(fid));
fclose(fid);
 
ne=fix(tmp1(1));
np=fix(tmp1(2));
 
fid=fopen(fname);
c1=textscan(fid,'%d%f%f%f',np,'headerLines',2);
fclose(fid);
 
fid=fopen(fname);
c2=textscan(fid,'%d%d%d%d%d%d',ne,'headerLines',2+np);
fclose(fid);
 
x=c1{2}(:);
y=c1{3}(:);
bathy=c1{4}(:);
i34=c2{2}(:);
 
nm(1:ne,1:4)=nan;
for i=1:ne
  for j=1:i34(i)
    nm(i,j)=fix(c2{j+2}(i));
  end %for j
end %for i
 
[lonm,latm]=my_project_NC_KB(x,y,'reverse');
 