% Parámetros del esferoide
%tamaños del utero a las 30 semanas de gestacion.
%Donde el bebe alcanza (90%) los 2.5kg. 
%{
[Verbruggen SW, Kainz B,]
Shelmerdine SC, Hajnal JV, Rutherford MA,
Arthurs OJ, Phillips ATM, Nowlan NC. 2018
Stresses and strains on the human fetal
skeleton during development. J. R. Soc.
Interface 15: 20170593.
http://dx.doi.org/10.1098/rsif.2017.0593
%}

%Medidas de los ejes
a = 178.29; % Radio en el eje x en mm (eje ecuatorial)
b = 178.29; % Radio en el eje y en mm (eje ecuatorial)
c = 236.29; % Radio en el eje z en mm (eje polar)

% Malla esférica
[u, v] = meshgrid(linspace(0, 2*pi, 50), linspace(0, pi, 50));

% Coordenadas paramétricas del esferoide
x = a * sin(v) .* cos(u);
y = b * sin(v) .* sin(u);
z = c * cos(v);

% Gráfica del esferoide
figure;
surf(x, y, z, 'FaceColor', 'cyan', 'EdgeColor', 'blue');
axis equal;
grid on;

% Opciones de visualización
xlabel('X-axis');
ylabel('Y-axis');
zlabel('Z-axis');
title('Esferoide Prolato');
camlight;
lighting phong;

% (Después de definir los parámetros del esferoide y graficarlo)
volumen = ((4/3) * pi) * a * b * c;

% Redondear a 2 decimales
volumen_entero = round(volumen);

%Convertir volumen a litros
volumen_litros =  volumen_entero / 1000000;
fprintf('El volumen del esferoide es %.2f litros.\n', volumen_litros);

% Parámetros del esferoide
%Volumen del utero de 30 semanas usando la Formula de Brun
%{
Aleksei Petrovich Petrenko , Camil Andreu Castelo Branco Flores ,
Dimitry Vasilevich Marshalov , Alexander Valerievich Kuligin , Yuliya Sergeevna Mysovskaya ,
Efim Munevich Shifman & Adam Muhamed Rasulovich Abdulaev (2020): Physiology of
intra‐abdominal volume during pregnancy, Journal of Obstetrics and Gynaecology, DOI:
10.1080/01443615.2020.1820470
%}


% Calcular volumen usando Formula de Brun. 
volumen_brun =  (a * b * c)*0.475;

% Redondear a 2 decimales
volumen_entero2 = round(volumen_brun);


%Formula de esferoide prolato con constante de ajuste. 
% Constantes
k = 0.28; % Factor de calibración ajustado empíricamente

% Calcular volumen usando la fórmula del esferoide prolato
volumen_teorico = (4/3) * pi * a * b * c;

% Calibrar el volumen
volumen_calibrado = k * volumen_teorico;

% Convertir volumen a litros
volumen_litros = volumen_calibrado / 1e6;

% Mostrar resultados
fprintf('El volumen Formula de Brun %.2f litros.\n', volumen_brun);
fprintf('Volumen con formula del esferoide prolato (sin calibrar): %.2f litros\n', volumen_teorico / 1e6);
fprintf('Volumen calibrado (ajustado): %.2f litros\n', volumen_litros);
