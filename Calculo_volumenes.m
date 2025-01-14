% Datos de los esferoides prolatos (Largo, Ancho, APD en mm)
data = [
    163.03, 163.03, 163.03;  % 20 semanas
    166.98, 166.98, 166.98;  % 25 semanas
    236.29, 178.29, 178.29; % 30 semanas
    219.49, 186.75, 186.75  % 35 semanas
];

% Inicialización de resultados
volumes_standard = zeros(size(data, 1), 1);
volumes_brun = zeros(size(data, 1), 1);

% Cálculo de volúmenes
for i = 1:size(data, 1)
    % Ejes mayores y menores
    a = data(i, 1) / 2;  % Semi-eje mayor
    b = data(i, 2) / 2;  % Semi-eje menor
    c = data(i, 3) / 2;  % Semi-eje menor (igual a b para prolato)
    
    % Volumen estándar del esferoide prolato
    volumes_standard(i) = (4/3) * pi * a * b^2;
    
    % Volumen usando la fórmula de Brun
    L = data(i, 1);  % Largo
    W = data(i, 2);  % Ancho
    APD = data(i, 3); % Diámetro anteroposterior
    volumes_brun(i) = (L * W * APD) * 0.457;
end

% Conversión a litros
volumes_standard_liters = volumes_standard / 1e6;
volumes_brun_liters = volumes_brun / 1e6;

% Mostrar resultados en litros
disp('Volúmenes calculados en litros:');
disp('--------------------------------');
for i = 1:size(data, 1)
    fprintf('Semana %d:\n', 20 + 5 * (i - 1));
    fprintf('  Volumen estándar: %.6f litros\n', volumes_standard_liters(i));
    fprintf('  Volumen (fórmula de Brun): %.6f litros\n', volumes_brun_liters(i));
    disp('--------------------------------');
end