# Valida o modelo semantico com o parser TMDL oficial do Power BI Desktop.
#
# O Power BI instala a assembly Microsoft.PowerBI.Tabular.dll junto com o app.
# Este script carrega essa assembly, chama DeserializeModelFromFolder e reporta
# o resultado real, em vez de confiar em inspecao visual do arquivo.
#
# Uso: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_tmdl.ps1
# Codigo de saida 0 quando o modelo passa, 1 quando falha ou quando o Power BI
# nao esta instalado.

param(
    [string]$DefinitionPath = (Join-Path $PSScriptRoot "..\dashboard_cana.SemanticModel\definition")
)

$ErrorActionPreference = "Continue"

$pacote = Get-AppxPackage Microsoft.MicrosoftPowerBIDesktop -ErrorAction SilentlyContinue
if (-not $pacote) {
    Write-Output "SKIP: Power BI Desktop nao esta instalado nesta maquina."
    exit 1
}

$bin = Join-Path $pacote.InstallLocation "bin"
$assembly = Join-Path $bin "Microsoft.PowerBI.Tabular.dll"
if (-not (Test-Path $assembly)) {
    Write-Output "SKIP: assembly do parser TMDL nao encontrada em $bin"
    exit 1
}

[System.AppDomain]::CurrentDomain.add_AssemblyResolve({
    param($sender, $args)
    $nome = ($args.Name -split ",")[0]
    $tentativa = Join-Path $bin ($nome + ".dll")
    if (Test-Path $tentativa) {
        try { return [System.Reflection.Assembly]::LoadFrom($tentativa) } catch { }
    }
    return $null
})

try {
    $asm = [System.Reflection.Assembly]::LoadFrom($assembly)
    $tipo = $asm.GetType("Microsoft.AnalysisServices.Tabular.TmdlSerializer")
    $metodo = $tipo.GetMethod("DeserializeModelFromFolder", [type[]]@([string]))
} catch {
    Write-Output ("SKIP: nao foi possivel carregar o parser. " + $_.Exception.Message)
    exit 1
}

$alvo = (Resolve-Path $DefinitionPath).Path
Write-Output ("Validando: " + $alvo)

try {
    $modelo = $metodo.Invoke($null, @($alvo))
} catch {
    $erro = $_.Exception
    while ($erro.InnerException) { $erro = $erro.InnerException }
    Write-Output "PARSE FALHOU"
    Write-Output $erro.Message
    exit 1
}

$tabelas = $modelo.Tables.Count
$medidas = 0
foreach ($tabela in $modelo.Tables) { $medidas += $tabela.Measures.Count }

Write-Output "PARSE OK"
foreach ($tabela in $modelo.Tables) {
    Write-Output ("  " + $tabela.Name + " | colunas=" + $tabela.Columns.Count + " medidas=" + $tabela.Measures.Count)
}
foreach ($rel in $modelo.Relationships) {
    Write-Output ("  relacao: " + $rel.FromTable.Name + "[" + $rel.FromColumn.Name + "] -> " +
                  $rel.ToTable.Name + "[" + $rel.ToColumn.Name + "]")
}
Write-Output ("Total: " + $tabelas + " tabelas, " + $medidas + " medidas, " + $modelo.Relationships.Count + " relacionamentos")
exit 0
