function alpha_beta_heatmap_alpha_partisan

load heatmap_mat

x = 0:0.01:1;
y = 1:-0.01:0;

figure1 = figure('color',[1 1 1]);
axes1 = axes('Parent',figure1,'FontSize',24);box(axes1,'on');hold(axes1,'on');
view(axes1,[26 24]);

% x = 0.2:0.2:6; % the weight changes of link A_23
% y = 0.2:0.2:6; % the weight changes of link A_24
[X,Y] = meshgrid(x,y);

xdata1 = X;
ydata1 = Y;
zdata1 = FE_b;
zdata2 = BE_b;
% zdata2(1,2)=0.94;

for i = 1:101
    try
        F_c(i) = min(find(zdata1(i,:)>0.8));  %
    catch
        F_c(i) = max(find(zdata1(i,:)<0.8));
    end
end

for i = 1:101
    try
        B_c(i) = min(find(zdata2(i,:)>0.8));  %
    catch
        B_c(i) = max(find(zdata2(i,:)<0.8));
    end
end

% Create surf
surf(xdata1,ydata1,zdata1,'Parent',axes1,'FaceAlpha',0.5,...
    'FaceColor',[1 0 0],...
    'EdgeColor','none');

% Create surf
surf(xdata1,ydata1,zdata2,'Parent',axes1,'FaceAlpha',0.5,...
    'FaceColor',[0 0 1],...
    'EdgeColor','none');

plot3(F_c*0.01, y, ones(101,1),'c','LineWidth',2)
plot3(B_c*0.01, y, ones(101,1),'g','LineWidth',2)
% Create zlabel
% zlabel('Estextremism');
% Create xlabel
% xlabel('\beta (Party identiy)');
xlim([0,1])
ylim([0,1])
xticks([0 .2 .4 .6 .8 1])
xticklabels({'', '', '', '', '', ''})
yticks([0 .2 .4 .6 .8 1])
yticklabels({'', '', '', '', '', ''})
zticks([0 .2 .4 .6 .8 1])
zticklabels({'', '', '', '', '', ''})
% Create ylabel
% ylabel('\alpha (intolerance)');


view(axes1,[-123.2 36.4000000000001]);
box(axes1,'on');
grid(axes1,'on');
