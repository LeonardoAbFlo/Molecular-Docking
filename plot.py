import streamlit as st
import os
import subprocess

st.title("Docking Molecular con AutoDock Vina")
st.text("Autor: Leonardo Marcelo Abanto-Florez")


st.header("Carga de archivos")
target_file = st.file_uploader("Sube el archivo de la proteína (PDBQT)", type=["pdbqt"])
ligand_file = st.file_uploader("Sube el archivo del ligando (PDBQT)", type=["pdbqt"])


st.sidebar.header("Parámetros de docking")
center_x = st.sidebar.number_input("Centro X", value=0.0)
center_y = st.sidebar.number_input("Centro Y", value=0.0)
center_z = st.sidebar.number_input("Centro Z", value=0.0)
size_x = st.sidebar.number_input("Tamaño X", value=20.0)
size_y = st.sidebar.number_input("Tamaño Y", value=20.0)
size_z = st.sidebar.number_input("Tamaño Z", value=20.0)
exhaustiveness = st.sidebar.slider("Exhaustividad", min_value=1, max_value=16, value=8)

vina_executable = r"C:\path\to\AutoDock-Vina\build\Release\vina.exe"


if st.button("Ejecutar Docking"):
    if target_file and ligand_file:
        target_path = os.path.join("uploads", target_file.name)
        ligand_path = os.path.join("uploads", ligand_file.name)

        os.makedirs("uploads", exist_ok=True)
        with open(target_path, "wb") as f:
            f.write(target_file.getbuffer())
        with open(ligand_path, "wb") as f:
            f.write(ligand_file.getbuffer())

        output_file = os.path.join("uploads", "result.pdbqt")
        vina_command = (
            f"{vina_executable} --receptor {target_path} --ligand {ligand_path} "
            f"--center_x {center_x} --center_y {center_y} --center_z {center_z} "
            f"--size_x {size_x} --size_y {size_y} --size_z {size_z} "
            f"--exhaustiveness {exhaustiveness} --out {output_file}"
        )

        st.write("Ejecutando AutoDock Vina...")
        process = subprocess.run(vina_command, shell=True, capture_output=True, text=True)

        if process.returncode == 0:
            st.success("Docking completado exitosamente.")
            st.text("Resultados:")
            with open(output_file, "r") as f:
                st.text(f.read())
        else:
            st.error("Error al ejecutar AutoDock Vina.")
            st.text(process.stderr)
    else:
        st.error("Por favor, sube tanto el archivo de la proteína como el del ligando.")


