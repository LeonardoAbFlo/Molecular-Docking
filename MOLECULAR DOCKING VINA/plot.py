import streamlit as st
import os
import subprocess
from rdkit import Chem
from rdkit.Chem import Draw

# Título de la aplicación
st.title("Web de Docking Molecular con AutoDock Vina")

# Sección de carga de archivos
st.header("Carga de archivos")
target_file = st.file_uploader("Sube el archivo de la proteína (PDBQT)", type=["pdbqt"])
ligand_file = st.file_uploader("Sube el archivo del ligando (PDBQT)", type=["pdbqt"])

# Visualización del ligando (opcional)
if ligand_file:
    st.write("Vista previa del ligando:")
    ligand = Chem.MolFromMolFile(ligand_file.name, removeHs=False)  # Asegúrate de cargar un archivo adecuado
    if ligand:
        st.image(Draw.MolToImage(ligand), caption="Estructura del ligando")

# Parámetros de docking
st.sidebar.header("Parámetros de Docking")
center_x = st.sidebar.number_input("Centro X", value=0.0)
center_y = st.sidebar.number_input("Centro Y", value=0.0)
center_z = st.sidebar.number_input("Centro Z", value=0.0)
size_x = st.sidebar.number_input("Tamaño X", value=20.0)
size_y = st.sidebar.number_input("Tamaño Y", value=20.0)
size_z = st.sidebar.number_input("Tamaño Z", value=20.0)
exhaustiveness = st.sidebar.slider("Exhaustividad", min_value=1, max_value=16, value=8)

# Ejecutar docking
if st.button("Ejecutar Docking"):
    if target_file and ligand_file:
        st.write("Ejecutando AutoDock Vina...")
        target_path = os.path.join("uploads", target_file.name)
        ligand_path = os.path.join("uploads", ligand_file.name)

        # Guardar los archivos subidos
        with open(target_path, "wb") as f:
            f.write(target_file.getbuffer())
        with open(ligand_path, "wb") as f:
            f.write(ligand_file.getbuffer())

        # Comando de AutoDock Vina
        output_file = "result.pdbqt"
        vina_command = (
            f"vina --receptor {target_path} --ligand {ligand_path} "
            f"--center_x {center_x} --center_y {center_y} --center_z {center_z} "
            f"--size_x {size_x} --size_y {size_y} --size_z {size_z} "
            f"--exhaustiveness {exhaustiveness} --out {output_file}"
        )

        # Ejecutar el comando
        process = subprocess.run(vina_command, shell=True, capture_output=True, text=True)
        if process.returncode == 0:
            st.success("Docking completado exitosamente.")
            st.write("Resultados guardados en:", output_file)

            # Mostrar los resultados
            with open(output_file, "r") as f:
                st.text(f.read())
        else:
            st.error("Error al ejecutar AutoDock Vina.")
            st.text(process.stderr)
    else:
        st.error("Por favor, sube tanto el archivo de la proteína como el del ligando.")

# Visualización del docking (opcional)
st.header("Visualización (pendiente)")
st.write("Para integrar una visualización 3D, puedes usar bibliotecas como `nglview`.")