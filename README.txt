Acest proiect a fost dezvoltat intr-un environment de Conda. In acest folder se poate gasi fisierul environment.yml
dupa care se poate crea environment-ul pe calculatorul dumneavoastra

De asemenea, aici este o lista de pachete pip folosite (versiune python 3.13.0)

joblib==1.4.2
numpy==2.1.3
opencv-python==4.10.0.84
scikit-learn==1.5.2
scipy==1.14.1
setuptools==75.1.0
threadpoolctl==3.5.0
wheel==0.44.0

Am testat fisierul environment.yml cu un nou environment si a functionat. Pentru instalarea pachetelor direct in pip nu am incercat.

Rularea proiectului se face din fisierul code/main.py. De acolo se pot modifica parametrii catre directoarele train/test, imaginile auxiliare
si numarul de jocuri pe care se va rula testarea. directorul de results, daca nu este creat, va fi implicit creat.

Folder-ul root din care ar trebui rulat proiectul se considera cel care contine foldererele code/ si imagini_auxiliare/

Datorita modului in care am conceput solutia, rularea din main a proiectului va genera fisiere solutie pentru toate cele
3 task-uri odata. Nu am testat individual fiecare task, ci le rezolv simultan.
