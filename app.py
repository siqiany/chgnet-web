from flask import Flask, request, jsonify
import tempfile
import werkzeug
import json
from chgnet.model.model import CHGNet
import numpy as np
from pymatgen.core import Structure
from chgnet.model.dynamics import MolecularDynamics
from chgnet.model import StructOptimizer
import traceback
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins":" *","allow_headers": ["Content-Type"],"allow_methods": ["POST"],"supports_credentials": True}})
logging.basicConfig(level=logging.DEBUG)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def deep_convert(obj):
    """
    递归地将所有 NumPy 类型转换为原生 Python 类型。
    """
    if isinstance(obj, np.bool_):  # 转换 NumPy 布尔类型
        return bool(obj)
    elif isinstance(obj, np.integer):  # 转换 NumPy 整数类型
        return int(obj)
    elif isinstance(obj, np.floating):  # 转换 NumPy 浮点数类型
        return float(obj)
    elif isinstance(obj, np.ndarray):  # 转换 NumPy 数组为 Python 列表
        return obj.tolist()
    elif isinstance(obj, dict):  # 递归处理字典
        return {key: deep_convert(value) for key, value in obj.items()}
    elif isinstance(obj, list):  # 递归处理列表
        return [deep_convert(item) for item in obj]
    elif isinstance(obj, tuple):  # 递归处理元组
        return tuple(deep_convert(item) for item in obj)
    return obj  # 非 NumPy 类型，直接返回

def process_structure(data):
    # 删除不需要的元数据
    if "@module" in data:
        del data["@module"]
    if "@class" in data:
        del data["@class"]

    # 处理 lattice 数据
    lattice = data["lattice"]
    lattice["pbc"] = list(lattice["pbc"])  # 转换元组为列表

    # 处理 sites 数据
    for site in data["sites"]:
        # 如果有需要进一步处理的信息，可以在这里操作
        site["species"] = [{"element": s["element"], "occu": s["occu"]} for s in site["species"]]

    return data

@app.route('/direct-inference', methods=['POST'])
def direct_inference():
    print("Request headers:", request.headers)
    data = request.get_data()
    print("请求体原始数据（部分展示，可能需要根据实际情况处理编码等问题）:", data[:100])
    print("请求体数据长度:", len(data))
    decoded_data = data.decode('utf-8')
    print("请求体数据解码后（部分展示）:", decoded_data[:100])
    if not data:
        return jsonify({"error": "接收到的请求体为空，请检查前端是否正确发送数据。"}), 400
    try:
        print("Request.files content:", request.files)
        file = request.files['file']
        if file.filename == '':
            print("Empty filename received in file upload.")
            return jsonify({"error": "Empty filename received in file upload."}), 400
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        # 手动添加.cif扩展名到临时文件名
        new_temp_file_path = temp_file_path + '.cif'
        os.rename(temp_file_path, new_temp_file_path)
        temp_file_path = new_temp_file_path
        # 使用添加扩展名后的临时文件路径调用Structure.from_file函数
        structure = Structure.from_file(temp_file_path)
        chgnet = CHGNet.load()
        prediction = chgnet.predict_structure(structure)
        result_output = ""
        for key, unit in [
            ("energy", "eV/atom"),
            ("forces", "eV/A"),
            ("stress", "GPa"),
            ("magmom", "mu_B"),
        ]:
            result_output += f"CHGNet-predicted {key} ({unit}):\n{prediction[key[0]]}\n\n"
        return jsonify(result_output)
    except werkzeug.exceptions.BadRequestKeyError as e:
        print(traceback.format_exc())
        return jsonify({"error": "File not found in the request. Please ensure the file is correctly attached."}), 400
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/molecular-dynamics', methods=['POST'])
def molecular_dynamics():
    print("Request headers:", request.headers)
    data = request.get_data()
    print("请求体原始数据（部分展示，可能需要根据实际情况处理编码等问题）:", data[:100])
    print("请求体数据长度:", len(data))
    decoded_data = data.decode('utf-8')
    print("请求体数据解码后（部分展示）:", decoded_data[:100])
    try:
        file = request.files['file']
        md_params = request.form.get('mdParams')
        md_params = json.loads(md_params)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
            # 手动添加.cif扩展名到临时文件名
        new_temp_file_path = temp_file_path + '.cif'
        os.rename(temp_file_path, new_temp_file_path)
        temp_file_path = new_temp_file_path
        # 使用添加扩展名后的临时文件路径调用Structure.from_file函数
        structure = Structure.from_file(temp_file_path)
        chgnet = CHGNet.load()
        if md_params['device'].lower() == 'cpu':
            use_device = 'cpu'
        else:
            use_device = 'cuda'
        md = MolecularDynamics(
            atoms=structure,
            model=chgnet,
            ensemble=md_params['ensemble'],
            temperature=md_params['temperature'],
            timestep=md_params['timestep'],
            trajectory=md_params['trajectory'],
            logfile=md_params['logfile'],
            loginterval=md_params['loginterval'],
            use_device=use_device
        )
        md.run(md_params['steps'])

        # 读取轨迹文件内容
        with open(md_params['trajectory'], 'rb') as traj_file:
            traj_data = traj_file.read()

        # 读取日志文件内容
        with open(md_params['logfile'], 'rb') as log_file:
            log_data = log_file.read()

        # 创建一个包含文件信息的字典，可以根据前端期望的格式进行调整
        response_data = {
            "message": "Molecular Dynamics simulation completed successfully.\n",
            "trajectory": {
                "name": os.path.basename(md_params['trajectory']),
                "content": traj_data.decode('latin-1') if isinstance(traj_data, bytes) else traj_data,
                "content_type": "application/octet-stream"
            },
            "logfile": {
                "name": os.path.basename(md_params['logfile']),
                "content": log_data.decode('latin-1') if isinstance(log_data, bytes) else log_data,
                "content_type": "application/octet-stream"
            }
        }

        return jsonify(response_data)
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/structure-optimization', methods=['POST'])
def structure_optimization():
    print("Request headers:", request.headers)
    data = request.get_data()
    print("请求体原始数据（部分展示，可能需要根据实际情况处理编码等问题）:", data[:100])
    print("请求体数据长度:", len(data))
    decoded_data = data.decode('utf-8')
    print("请求体数据解码后（部分展示）:", decoded_data[:100])
    if not data:
        return jsonify({"error": "接收到的请求体为空，请检查前端是否正确发送数据。"}), 400
    try:
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "文件名不能为空，请确保文件正确上传。"}), 300
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        # 手动添加.cif扩展名到临时文件名
        new_temp_file_path = temp_file_path + '.cif'
        os.rename(temp_file_path, new_temp_file_path)
        temp_file_path = new_temp_file_path
        # 使用添加扩展名后的临时文件路径调用Structure.from_file函数
        structure = Structure.from_file(temp_file_path)
        relaxer = StructOptimizer()
        result = relaxer.relax(structure)
        final_structure = result["final_structure"]
        relaxed_total_energy = result['trajectory'].energies[-1]
        final_structure_result=deep_convert(final_structure.as_dict())
        final_structure_result=process_structure(final_structure_result)
        relaxed_total_energy=deep_convert(relaxed_total_energy)
        return jsonify({
            "final_structure": final_structure_result,
            "relaxed_total_energy": relaxed_total_energy,
            "message": "结构优化处理完成"
        })
    except werkzeug.exceptions.BadRequestKeyError as e:
        print(traceback.format_exc())
        return jsonify({"error": "未在请求中找到文件，请检查文件是否正确添加到请求中并重新发送。"}), 400
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
