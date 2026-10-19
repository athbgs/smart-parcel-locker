"""Optional advanced test harness; separate from the introductory-course program."""
import ast
import builtins
import contextlib
import hashlib
import io
import itertools
import json
from pathlib import Path
import time
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "WI1102_ProjekI_31_12.py"
TEXT = SOURCE.read_text()
TREE = ast.parse(TEXT)
PROGRAM = compile(TEXT, str(SOURCE), "exec")
RESULTS = []
RUN_STARTED_AT = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat()


def run_program(values):
    values = iter(values)
    output = io.StringIO()
    prompts = []
    namespace = {"__name__": "__main__"}

    def read_input(prompt=""):
        try:
            value = next(values)
        except StopIteration as exc:
            raise AssertionError("Unexpected input prompt: " + prompt) from exc
        prompts.append(prompt)
        print(prompt + value)
        return value

    custom_builtins = dict(vars(builtins))
    custom_builtins["input"] = read_input
    namespace["__builtins__"] = custom_builtins
    with contextlib.redirect_stdout(output):
        exec(PROGRAM, namespace)
    assert next(values, None) is None, "Unused test input"
    assert namespace["berjalan"] is False
    active_codes = []
    for i in range(6):
        if namespace["status"][i] == "Kosong":
            assert all(namespace[k][i] == "" for k in ("nama", "telepon", "kode"))
        else:
            assert namespace["status"][i] == "Terisi"
            assert all(namespace[k][i] != "" for k in ("nama", "telepon", "kode"))
            active_codes.append(namespace["kode"][i])
    assert len(set(active_codes)) == len(active_codes), "Duplicate active code"
    return namespace, output.getvalue(), prompts


def deposit(dimensions=(10, 10, 10), name="Ana", phone="081234", pay="y"):
    return ["1", *(str(v) for v in dimensions), name, phone, pay]


def case(name, inputs, check, purpose):
    start = time.monotonic()
    try:
        state, output, prompts = run_program(inputs)
        check(state, output, prompts)
        RESULTS.append({
            "name": name, "result": "PASS", "purpose": purpose,
            "elapsed_seconds": round(time.monotonic() - start, 6),
            "inputs": inputs, "output": output,
            "final_state": {k: state[k] for k in
                            ("status", "nama", "telepon", "kode", "nomor_kode")},
        })
    except Exception as exc:
        RESULTS.append({"name": name, "result": "FAIL", "purpose": purpose,
                        "error": repr(exc), "inputs": inputs})


def require(condition, message="Check failed"):
    assert condition, message


case("initial_status", ["3", "4"],
     lambda s, o, p: require("Total kosong: 6" in o and "Total terisi: 0" in o
                            and "Kosong D: 2 | C: 2 | B: 1 | A: 1" in o),
     "Enam loker awal kosong; jumlah setiap tipe sesuai inventori.")
case("retrieve_empty", ["2", "4"],
     lambda s, o, p: require("Tidak ada paket tersimpan." in o and len(p) == 2),
     "Ambil saat semua loker kosong kembali ke menu tanpa meminta kode.")

for kind, dimensions, index in [
    ("D", (30, 20, 45), 0), ("C", (30, 30, 45), 2),
    ("B", (30, 40, 45), 4), ("A", (20, 60, 45), 5),
]:
    case("exact_fit_" + kind, deposit(dimensions) + ["4"],
         lambda s, o, p, i=index: require(s["kode"][i] == "P1001"
                                           and s["nama"][i] == "Ana"
                                           and s["telepon"][i] == "081234"),
         "Paket tepat batas dimensi tipe " + kind + " tersimpan di loker yang benar.")

case("oversize", ["1", "60", "60", "60", "4"],
     lambda s, o, p: require(s["status"] == ["Kosong"] * 6
                            and "Tidak ada loker kosong yang cukup" in o),
     "Setiap sisi 60 cm valid, tetapi paket 60 x 60 x 60 tidak muat; data tetap kosong.")
invalid_dims = ["", "abc", "-1", "0", "1.5", " 20", "1e2", "nan", "１２"]
case("invalid_dimensions", ["1"] + invalid_dims + ["20", "0", "20", "-2", "20",
                                                     "Ana", "081234", "y", "4"],
     lambda s, o, p: require(o.count("Ukuran harus bilangan bulat 1-60 cm") == 11
                            and s["kode"][0] == "P1001"),
     "Kosong, teks, negatif, nol, pecahan, spasi, notasi eksponen, dan angka non-ASCII ditolak.")
case("overlong_dimension", ["1", "10000", "9" * 5000, "20", "20", "20",
                            "Ana", "081234", "y", "4"],
     lambda s, o, p: require(o.count("Ukuran harus bilangan bulat 1-60 cm") == 2
                            and s["kode"][0] == "P1001"),
     "Nilai 10000 dan 5.000 digit sembilan ditolak dengan aman; input berikutnya berhasil.")
case("blank_metadata", ["1", "10", "10", "10", "", " ", "\t", "Ana",
                        "", "  ", "\t", "081234", "y", "4"],
     lambda s, o, p: require(o.count("Isian tidak boleh kosong") == 6
                            and s["nama"][0] == "Ana" and s["telepon"][0] == "081234"),
     "Nama dan telepon kosong, hanya spasi, atau hanya tab wajib diisi ulang.")
case("cancel_deposit", deposit(pay="t") + deposit(name="Budi") + ["4"],
     lambda s, o, p: require(s["kode"][0] == "P1001" and s["nomor_kode"] == 1002
                            and s["nama"][0] == "Budi" and s["kode"][1] == ""),
     "Pembatalan pembayaran tidak memakai slot atau menghabiskan kode.")
case("invalid_payment", deposit()[:-1] + ["yes", "", "y", "4"],
     lambda s, o, p: require(o.count("Jawaban harus y atau t.") == 2
                            and s["kode"][0] == "P1001"),
     "Pilihan pembayaran tidak valid diulang hingga y/t.")
case("retrieve_success", deposit() + ["2", "P1001", "y", "4"],
     lambda s, o, p: require(s["status"] == ["Kosong"] * 6
                            and "Paket diambil. L01 kosong." in o),
     "Pengambilan benar mereset status, nama, telepon, dan kode.")
case("wrong_code", deposit() + ["2", "SALAH", "3", "4"],
     lambda s, o, p: require(s["kode"][0] == "P1001"
                            and "Kode tidak ditemukan atau sudah digunakan." in o
                            and "Total terisi: 1" in o),
     "Kode salah tidak mengubah data dan kembali ke menu; tidak ada loop tak berujung.")
case("cancel_retrieval", deposit() + ["2", "P1001", "t", "4"],
     lambda s, o, p: require(s["kode"][0] == "P1001" and s["nama"][0] == "Ana"
                            and "Pengambilan dibatalkan." in o),
     "Pembatalan pengambilan mempertahankan seluruh data paket.")
case("invalid_retrieval_confirmation", deposit() + ["2", "P1001", "ya", "y", "4"],
     lambda s, o, p: require(s["status"][0] == "Kosong"
                            and o.count("Jawaban harus y atau t.") == 1),
     "Konfirmasi pengambilan diulang ketika pilihan bukan y/t.")
case("stale_code", deposit() + deposit(name="Budi")
     + ["2", "P1001", "y", "2", "P1001", "4"],
     lambda s, o, p: require(s["kode"][0] == "" and s["kode"][1] == "P1002"
                            and o.count("Kode tidak ditemukan atau sudah digunakan.") == 1),
     "Kode yang sudah dipakai ditolak saat paket lain masih tersimpan.")
case("reuse_slot", deposit() + ["2", "P1001", "y"] + deposit(name="Citra")
     + ["2", "P1001", "4"],
     lambda s, o, p: require(s["kode"][0] == "P1002" and s["nama"][0] == "Citra"
                            and s["nomor_kode"] == 1003
                            and "Kode tidak ditemukan atau sudah digunakan." in o),
     "Loker bekas digunakan kembali dengan kode baru; kode lama tetap tidak berlaku.")
case("capacity_six", sum((deposit(name="Penerima " + str(i)) for i in range(6)), [])
     + ["1", "10", "10", "10", "3", "4"],
     lambda s, o, p: require(s["status"] == ["Terisi"] * 6
                            and s["kode"] == ["P" + str(n) for n in range(1001, 1007)]
                            and "Total kosong: 0" in o and "Total terisi: 6" in o
                            and "Tidak ada loker kosong yang cukup" in o),
     "Enam titip mengisi enam slot unik; paket ketujuh ditolak ketika penuh.")
case("fallback_after_D_full", deposit() + deposit() + deposit() + ["4"],
     lambda s, o, p: require(s["kode"][:3] == ["P1001", "P1002", "P1003"]
                            and "Loker terpilih: L03 | Tipe: C" in o),
     "Ketika dua D penuh, paket kecil beralih ke C yang kosong.")
case("B_A_tie_and_fallback", deposit((20, 40, 45)) + deposit((20, 40, 45)) + ["4"],
     lambda s, o, p: require(s["kode"][4:] == ["P1001", "P1002"]),
     "Paket yang muat B/A memilih B lebih dahulu lalu A ketika B penuh.")
case("invalid_menu", ["foo", "0", "", "4"],
     lambda s, o, p: require(o.count("Menu tidak valid.") == 3),
     "Menu tidak valid diulang dan pilihan keluar menghentikan program.")
case("mixed_status", deposit((20, 20, 20)) + deposit((30, 30, 45))
     + deposit((30, 40, 45)) + ["2", "P1002", "y", "3", "4"],
     lambda s, o, p: require("Total kosong: 4" in o and "Total terisi: 2" in o
                            and "Kosong D: 1 | C: 2 | B: 0 | A: 1" in o),
     "Status dan hitungan setiap tipe konsisten setelah titip dan ambil campuran.")
case("independent_packages", deposit(name="Ana") + deposit(name="Budi")
     + ["2", "P1002", "y", "4"],
     lambda s, o, p: require(s["nama"][0] == "Ana" and s["kode"][0] == "P1001"
                            and s["nama"][1] == "" and s["status"][1] == "Kosong"),
     "Mengambil paket kedua tidak mengubah data paket pertama.")

for kind, dimensions, index in [("B", (30, 40, 45), 4), ("A", (20, 60, 45), 5)]:
    for number, permutation in enumerate(itertools.permutations(dimensions), 1):
        case("rotation_" + kind + "_" + str(number), deposit(permutation) + ["4"],
             lambda s, o, p, i=index: require(s["kode"][i] == "P1001"),
             "Rotasi " + str(permutation) + " tetap memilih tipe " + kind + ".")

# Dimension regressions are written before changing the main program (TDD).
dimension_labels = ["Panjang", "Lebar", "Tinggi"]
dimension_prompts = [label + " paket (bulat 1-60 cm): " for label in dimension_labels]

case("dimension_prompts_match_inventory", deposit((60, 45, 20)) + ["4"],
     lambda s, o, p: require(p[1:4] == dimension_prompts
                            and s["kode"][5] == "P1001"),
     "Ketiga prompt menyebut 1-60 cm dan paket 60 x 45 x 20 tetap masuk A lewat rotasi.")

for axis, label in enumerate(dimension_labels):
    retry_inputs = ["20"] * axis + ["61", "20"] + ["20"] * (2 - axis)
    case("over_limit_61_" + label.lower(),
         ["1"] + retry_inputs + ["Ana", "081234", "t", "4"],
         lambda s, o, p, a=axis: require(
             o.count("Ukuran harus bilangan bulat 1-60 cm") == 1
             and p[1 + a:3 + a] == [dimension_prompts[a]] * 2
             and s["status"] == ["Kosong"] * 6 and s["nomor_kode"] == 1001),
         label + " 61 cm ditolak dan diulang pada dimensi yang sama; batal tidak mengubah data.")

case("over_limit_9999", ["1", "9999", "20", "20", "20", "Ana", "081234", "t", "4"],
     lambda s, o, p: require(o.count("Ukuran harus bilangan bulat 1-60 cm") == 1
                            and p[1:3] == [dimension_prompts[0]] * 2
                            and s["status"] == ["Kosong"] * 6
                            and s["nomor_kode"] == 1001),
     "Batas lama 9999 ditolak langsung pada input panjang; tidak ada transaksi tersimpan.")

case("leading_zero_rotated_60", deposit(("00060", "00045", "00020")) + ["4"],
     lambda s, o, p: require(s["kode"][5] == "P1001" and s["dimensi"] == [60, 45, 20]
                            and "Ukuran harus" not in o),
     "Nol di depan tidak mengubah nilai; 00060 tetap valid dan rotasi memilih A.")

case("long_leading_zero_60", deposit(("0" * 4998 + "60", "20", "45")) + ["4"],
     lambda s, o, p: require(s["kode"][5] == "P1001" and s["dimensi"] == [60, 20, 45]
                            and "Ukuran harus" not in o),
     "5.000 karakter dengan nol di depan dan nilai 60 diterima tanpa konversi string panjang.")

case("zero_only_dimension", ["1", "0" * 5000, "1", "1", "1", "Ana", "081234", "y", "4"],
     lambda s, o, p: require(o.count("Ukuran harus bilangan bulat 1-60 cm") == 1
                            and p[1:3] == [dimension_prompts[0]] * 2
                            and s["dimensi"] == [1, 1, 1] and s["kode"][0] == "P1001"),
     "5.000 angka nol tetap bernilai nol dan ditolak; batas bawah 1 cm diterima.")

# Reuse the exact source allocation loop and compare against an independent oracle.
allocation = next(node for node in ast.walk(TREE) if isinstance(node, ast.For)
                  and any(isinstance(x, ast.Assign)
                          and isinstance(x.targets[0], ast.Name)
                          and x.targets[0].id == "muat" for x in node.body))
allocation_program = compile(ast.Module(body=[allocation], type_ignores=[]),
                             "<original allocation loop>", "exec")
boxes = [(30, 20, 45), (30, 20, 45), (30, 30, 45),
         (30, 30, 45), (30, 40, 45), (20, 60, 45)]
boundary_values = [1, 19, 20, 21, 29, 30, 31, 39, 40, 41, 44, 45, 46, 59, 60, 61]
geometry_checks = 0
geometry_failures = []
for dimensions in itertools.product(boundary_values, repeat=3):
    fits = [any(all(side <= bound for side, bound in zip(rotation, box))
                for rotation in itertools.permutations(dimensions)) for box in boxes]
    for mask in range(64):
        occupancy = ["Terisi" if mask & (1 << i) else "Kosong" for i in range(6)]
        expected = next((i for i in range(6) if fits[i] and occupancy[i] == "Kosong"), -1)
        state = {"p": dimensions[0], "l": dimensions[1], "t": dimensions[2],
                 "sisi_h": [box[0] for box in boxes], "sisi_v": [box[1] for box in boxes],
                 "sisi_d": [box[2] for box in boxes], "status": occupancy, "indeks": -1}
        exec(allocation_program, state)
        geometry_checks += 1
        if state["indeks"] != expected:
            geometry_failures.append({"dimensions": dimensions, "mask": mask,
                                      "expected": expected, "actual": state["indeks"]})

allowed_calls = {"print", "input", "range", "str", "int"}
calls = {node.func.id for node in ast.walk(TREE)
         if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
forbidden_nodes = (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef,
                   ast.Dict, ast.Set, ast.ListComp, ast.SetComp, ast.DictComp,
                   ast.GeneratorExp, ast.Try, ast.Break, ast.Continue)
syntax_check = {
    "allowed_calls_only": calls <= allowed_calls,
    "actual_calls": sorted(calls),
    "forbidden_constructs": [type(node).__name__ for node in ast.walk(TREE)
                             if isinstance(node, forbidden_nodes)],
    "max_line_width": max(map(len, TEXT.splitlines())),
    "source_lines": len(TEXT.splitlines()),
    "list_literals": sum(isinstance(node, ast.List) for node in ast.walk(TREE)),
    "for_loops": sum(isinstance(node, ast.For) for node in ast.walk(TREE)),
    "while_loops": sum(isinstance(node, ast.While) for node in ast.walk(TREE)),
}
all_passed = (all(item["result"] == "PASS" for item in RESULTS)
              and not geometry_failures and syntax_check["allowed_calls_only"]
              and not syntax_check["forbidden_constructs"]
              and syntax_check["max_line_width"] <= 90)
report = {
    "source": SOURCE.name, "sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "test_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "started_at": RUN_STARTED_AT,
    "finished_at": datetime.now(ZoneInfo("Asia/Jakarta")).isoformat(),
    "behavioral_scenarios": len(RESULTS),
    "behavioral_passed": sum(item["result"] == "PASS" for item in RESULTS),
    "geometry_dimension_triples": len(boundary_values) ** 3,
    "occupancy_patterns_per_triple": 64,
    "geometry_occupancy_checks": geometry_checks,
    "geometry_failures": geometry_failures,
    "course_syntax": syntax_check, "all_passed": all_passed, "scenarios": RESULTS,
    "limitations": [
        "Automated tests use scripted terminal input; not a user usability study.",
        "Geometry models rectangular boxes with six axis-aligned rotations.",
        "Inventory, dimensions, and counts are simulation assumptions.",
        "No physical door, sensor, payment, notification, or persistence was tested.",
        "Code uniqueness is guaranteed within one session; restarting resets data.",
    ],
}
(ROOT / "code_test_results.json").write_text(json.dumps(report, indent=2))
summary = [
    "HASIL UJI PROGRAM SMART LOCKER", "Waktu mulai: " + RUN_STARTED_AT,
    "Sumber: WI1102_ProjekI_31_12.py", "SHA-256: " + report["sha256"], "",
    f"Skenario perilaku: {report['behavioral_passed']}/{len(RESULTS)} lulus.",
    f"Geometri dan okupansi: {geometry_checks} pemeriksaan; "
    f"{len(geometry_failures)} ketidaksesuaian.",
    "Pemeriksaan terdiri atas 4.096 kombinasi ukuran x 64 pola terisi/kosong.",
    "Dua belas skenario menguji enam rotasi B dan enam rotasi A.",
    "Delapan regresi baru memeriksa batas input, pengulangan dimensi, dan nol di depan.",
    "Nilai 61 dalam pemeriksaan blok geometri adalah kasus negatif, bukan input CLI yang diterima.",
    "Seluruh skenario juga memeriksa data loker kosong dan keunikan kode aktif.",
    "Kesesuaian sintaks dasar: " + ("LULUS" if all_passed else "PERIKSA HASIL"), "",
]
summary += [f"{i:02d}. {item['result']} | {item['name']} | {item['purpose']}"
            for i, item in enumerate(RESULTS, 1)]
summary += ["", "BATASAN", *report["limitations"]]
(ROOT / "Hasil_Uji_Program.txt").write_text("\n".join(summary) + "\n")
print(json.dumps({key: value for key, value in report.items()
                  if key not in ("scenarios", "limitations")}, indent=2))
for result in RESULTS:
    if result["result"] != "PASS":
        print(json.dumps(result, indent=2))
raise SystemExit(0 if all_passed else 1)
