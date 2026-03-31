import React, { useMemo, useState } from "react"; import { motion } from "framer-motion"; import { Card, CardContent, CardDescription, CardHeader, CardTitle, } from "@/components/ui/card"; import { Button } from "@/components/ui/button"; import { Input } from "@/components/ui/input"; import { Label } from "@/components/ui/label"; import { Textarea } from "@/components/ui/textarea"; import { Badge } from "@/components/ui/badge"; import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"; import { Slider } from "@/components/ui/slider"; import { Progress } from "@/components/ui/progress"; import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, } from "recharts"; import { Search, Landmark, Layers3, ShieldCheck, Sparkles, ChevronRight, Scale, Network, BookOpen, ArrowRight, Binary, Cpu, } from "lucide-react";

const DIMENSIONS = [ { key: "customerBreadth", label: "Customer Breadth", short: "Breadth", description: "Does this asset serve one participant, a narrow niche, or many participants across the market?", left: "One participant", right: "Many participants", weight: 1.3, }, { key: "dependencyDepth", label: "Dependency Depth", short: "Dependency", description: "How deeply do customers depend on this asset inside workflows, operations, or supply chains?", left: "Optional", right: "Mission-critical", weight: 1.25, }, { key: "recurrence", label: "Recurring Demand", short: "Recurrence", description: "Is demand one-time, episodic, or structurally recurring?", left: "One-time", right: "Recurring", weight: 1.15, }, { key: "hiddenUtility", label: "Hidden Utility", short: "Utility", description: "Does value come from spectacle and visibility, or from quiet utility beneath the visible layer?", left: "Visible / hype", right: "Hidden / structural", weight: 0.95, }, { key: "switchingCost", label: "Switching Cost", short: "Switching", description: "Once integrated, how costly is it for customers to replace it?", left: "Easy to replace", right: "Hard to replace", weight: 1.1, }, { key: "standardPower", label: "Access / Standard Power", short: "Control", description: "Does the asset influence standards, permissions, distribution, pricing rails, or access?", left: "No standard power", right: "Defines access", weight: 1.5, }, { key: "outcomeExposure", label: "Outcome Dependence", short: "Exposure", description: "How dependent is the asset on winning one uncertain outcome versus serving many outcomes regardless of who wins?", left: "Depends on one winner", right: "Works regardless", weight: 1.35, }, { key: "capitalIntensity", label: "Capital / Infrastructure Density", short: "Density", description: "Does the asset sit close to infrastructure, logistics, compute, energy, or heavy operational rails?", left: "Light layer", right: "Dense infrastructure", weight: 1.0, }, ];

const PRESETS = { "OpenAI API": { customerBreadth: 88, dependencyDepth: 79, recurrence: 90, hiddenUtility: 72, switchingCost: 58, standardPower: 70, outcomeExposure: 82, capitalIntensity: 64, notes: "Serves many builders across use cases. Strong recurring demand and ecosystem leverage, though standard-setting power is meaningful rather than absolute.", }, NVIDIA: { customerBreadth: 83, dependencyDepth: 95, recurrence: 84, hiddenUtility: 87, switchingCost: 80, standardPower: 78, outcomeExposure: 86, capitalIntensity: 97, notes: "A classic shovel-layer asset: dense infrastructure relevance, deep dependency, and broad exposure to the whole rush rather than one narrow outcome.", }, "Vertical AI App": { customerBreadth: 34, dependencyDepth: 41, recurrence: 58, hiddenUtility: 29, switchingCost: 33, standardPower: 18, outcomeExposure: 25, capitalIntensity: 21, notes: "Often an extraction-layer bet: visible, narrow, and heavily exposed to whether one use case wins commercially.", }, Stripe: { customerBreadth: 86, dependencyDepth: 88, recurrence: 95, hiddenUtility: 84, switchingCost: 76, standardPower: 82, outcomeExposure: 91, capitalIntensity: 67, notes: "Strong infrastructure and control-layer behavior: embedded, recurring, and close to access and flow rather than one visible outcome.", }, };

const DEFAULT_VALUES = { customerBreadth: 50, dependencyDepth: 50, recurrence: 50, hiddenUtility: 50, switchingCost: 50, standardPower: 50, outcomeExposure: 50, capitalIntensity: 50, };

function clamp(n, min, max) { return Math.max(min, Math.min(max, n)); }

function scoreModel(values) { const weightedAverage = DIMENSIONS.reduce((sum, d) => sum + values[d.key] * d.weight, 0) / DIMENSIONS.reduce((sum, d) => sum + d.weight, 0);

const extractionScore = clamp( (100 - values.customerBreadth) * 0.18 + (100 - values.outcomeExposure) * 0.22 + (100 - values.standardPower) * 0.12 + (100 - values.hiddenUtility) * 0.14 + (100 - values.dependencyDepth) * 0.16 + (100 - values.switchingCost) * 0.08 + (100 - values.capitalIntensity) * 0.1, 0, 100 );

const shovelScore = clamp( values.customerBreadth * 0.17 + values.dependencyDepth * 0.18 + values.recurrence * 0.16 + values.hiddenUtility * 0.1 + values.switchingCost * 0.09 + values.outcomeExposure * 0.18 + values.capitalIntensity * 0.12, 0, 100 );

const gatekeeperScore = clamp( values.standardPower * 0.3 + values.switchingCost * 0.14 + values.dependencyDepth * 0.14 + values.customerBreadth * 0.12 + values.recurrence * 0.1 + values.hiddenUtility * 0.08 + values.outcomeExposure * 0.12, 0, 100 );

const sorted = [ { key: "Extraction", score: extractionScore }, { key: "Shovel", score: shovelScore }, { key: "Gatekeeper", score: gatekeeperScore }, ].sort((a, b) => b.score - a.score);

const primary = sorted[0].key; const spread = sorted[0].score - sorted[1].score;

let confidence = "Moderate"; if (spread >= 18) confidence = "High"; if (spread >= 30) confidence = "Very High"; if (spread <= 8) confidence = "Mixed";

const layer = gatekeeperScore >= 74 ? "Control Layer" : shovelScore >= extractionScore ? "Infrastructure Layer" : "Extraction Layer";

const strengths = DIMENSIONS.map((d) => ({ key: d.key, label: d.label, value: values[d.key], })) .sort((a, b) => b.value - a.value) .slice(0, 3);

const weaknesses = DIMENSIONS.map((d) => ({ key: d.key, label: d.label, value: values[d.key], })) .sort((a, b) => a.value - b.value) .slice(0, 3);

const narrative = buildNarrative({ primary, layer, confidence, weightedAverage, strengths, weaknesses, extractionScore, shovelScore, gatekeeperScore, });

return { weightedAverage: Math.round(weightedAverage), extractionScore: Math.round(extractionScore), shovelScore: Math.round(shovelScore), gatekeeperScore: Math.round(gatekeeperScore), primary, layer, confidence, strengths, weaknesses, narrative, }; }

function buildNarrative({ primary, layer, confidence, weightedAverage, strengths, weaknesses, extractionScore, shovelScore, gatekeeperScore, }) { const top = strengths.map((s) => s.label).join(", "); const bottom = weaknesses.map((w) => w.label).join(", ");

const primaryText = { Extraction: "This asset behaves primarily like an extraction-layer bet. It appears more dependent on winning a visible outcome than on quietly enabling the wider market.", Shovel: "This asset behaves primarily like a shovel. It captures value by serving many participants, embedding into operations, and benefiting from demand that persists regardless of who wins the visible race.", Gatekeeper: "This asset behaves primarily like a gatekeeper. Its strongest economic position comes from defining access, distribution, standards, or permissions rather than merely serving demand.", }[primary];

const layerText = { "Extraction Layer": "It sits closest to the layer where participants compete directly for outcomes.", "Infrastructure Layer": "It sits closest to the infrastructure layer where durable value is built beneath visible competition.", "Control Layer": "It sits closest to the control layer where durable power compounds through standards, access, and system leverage.", }[layer];

return { headline: ${primary} classification with ${confidence.toLowerCase()} confidence, body: ${primaryText} ${layerText} Its composite structural score is ${weightedAverage}/100. The strongest signals are ${top}. The weakest signals are ${bottom}. In ShovelsSale terms: this is not merely a product profile — it is a position within the market structure., brief: [ Extraction: ${extractionScore}, Shovel: ${shovelScore}, Gatekeeper: ${gatekeeperScore}, ], }; }

function SectionEyebrow({ children }) { return ( <div className="mb-4 flex items-center gap-3 text-[11px] uppercase tracking-[0.35em] text-amber-400/80"> <span className="h-px w-10 bg-amber-400/40" /> <span>{children}</span> </div> ); }

function MetricCard({ title, value, subtitle }) { return ( <Card className="rounded-3xl border-white/10 bg-white/5 backdrop-blur-xl"> <CardHeader className="pb-2"> <CardDescription className="text-xs uppercase tracking-[0.22em] text-zinc-400"> {title} </CardDescription> </CardHeader> <CardContent> <div className="text-3xl font-semibold text-zinc-50">{value}</div> <p className="mt-2 text-sm leading-6 text-zinc-400">{subtitle}</p> </CardContent> </Card> ); }

export default function ShovelScannerReferenceSystem() { const [assetName, setAssetName] = useState("NVIDIA"); const [category, setCategory] = useState("Compute Infrastructure"); const [notes, setNotes] = useState( "Dense infrastructure exposure, broad customer dependence, and recurring relevance across the whole AI market." ); const [values, setValues] = useState(PRESETS["NVIDIA"] || DEFAULT_VALUES);

const scores = useMemo(() => scoreModel(values), [values]);

const radarData = DIMENSIONS.map((d) => ({ dimension: d.short, score: values[d.key], }));

const classBars = [ { name: "Extraction", score: scores.extractionScore }, { name: "Shovel", score: scores.shovelScore }, { name: "Gatekeeper", score: scores.gatekeeperScore }, ];

function updateValue(key, newValue) { setValues((prev) => ({ ...prev, [key]: newValue[0] })); }

function applyPreset(name) { const preset = PRESETS[name]; if (!preset) return; setAssetName(name); setValues({ customerBreadth: preset.customerBreadth, dependencyDepth: preset.dependencyDepth, recurrence: preset.recurrence, hiddenUtility: preset.hiddenUtility, switchingCost: preset.switchingCost, standardPower: preset.standardPower, outcomeExposure: preset.outcomeExposure, capitalIntensity: preset.capitalIntensity, }); setNotes(preset.notes); }

return ( <div className="min-h-screen bg-zinc-950 text-zinc-100"> <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(circle_at_top_right,rgba(251,191,36,0.12),transparent_30%),radial-gradient(circle_at_20%_20%,rgba(251,191,36,0.08),transparent_25%)]" />

<div className="relative mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
    <motion.section
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.55 }}
      className="overflow-hidden rounded-[2rem] border border-white/10 bg-white/[0.04] shadow-2xl backdrop-blur-xl"
    >
      <div className="grid gap-10 px-6 py-10 md:px-10 lg:grid-cols-[1.15fr_0.85fr] lg:py-14">
        <div>
          <SectionEyebrow>ShovelsSale Reference System</SectionEyebrow>
          <h1 className="max-w-4xl text-5xl font-semibold leading-none tracking-tight text-zinc-50 sm:text-6xl lg:text-7xl">
            The <span className="text-amber-400">Shovel Scanner</span>
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-zinc-300">
            A sovereign-grade classification engine for evaluating whether any company,
            product, protocol, or digital asset belongs to the Extraction Layer, the
            Infrastructure Layer, or the Control Layer. This is not content. It is a
            decision system.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Badge className="rounded-full border border-amber-400/30 bg-amber-400/10 px-4 py-1.5 text-xs uppercase tracking-[0.24em] text-amber-300 hover:bg-amber-400/10">
              Economic Classification
            </Badge>
            <Badge className="rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-xs uppercase tracking-[0.24em] text-zinc-300 hover:bg-white/5">
              Market Structure Analysis
            </Badge>
            <Badge className="rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-xs uppercase tracking-[0.24em] text-zinc-300 hover:bg-white/5">
              Reference-Grade Methodology
            </Badge>
          </div>
          <div className="mt-10 grid gap-4 sm:grid-cols-3">
            <MetricCard
              title="Primary Class"
              value={scores.primary}
              subtitle="Dominant economic behavior under the ShovelsSale model."
            />
            <MetricCard
              title="Layer"
              value={scores.layer}
              subtitle="The structural position where value is primarily captured."
            />
            <MetricCard
              title="Composite Score"
              value={`${scores.weightedAverage}/100`}
              subtitle="Weighted structural strength across core Shovel dimensions."
            />
          </div>
        </div>

        <Card className="rounded-[2rem] border-white/10 bg-zinc-950/60 backdrop-blur-xl">
          <CardHeader>
            <CardTitle className="flex items-center gap-3 text-2xl text-zinc-50">
              <Search className="h-6 w-6 text-amber-400" />
              Scanner Input
            </CardTitle>
            <CardDescription className="text-zinc-400">
              Evaluate a target asset using structural rather than promotional criteria.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="assetName">Asset / Company</Label>
                <Input
                  id="assetName"
                  value={assetName}
                  onChange={(e) => setAssetName(e.target.value)}
                  className="border-white/10 bg-white/5"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="category">Category</Label>
                <Input
                  id="category"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="border-white/10 bg-white/5"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="notes">Analyst Notes</Label>
              <Textarea
                id="notes"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="min-h-[110px] border-white/10 bg-white/5"
              />
            </div>

            <div>
              <Label className="mb-3 block">Quick Presets</Label>
              <div className="flex flex-wrap gap-2">
                {Object.keys(PRESETS).map((name) => (
                  <Button
                    key={name}
                    type="button"
                    variant="outline"
                    className="rounded-full border-white/10 bg-white/5 text-zinc-200 hover:bg-white/10"
                    onClick={() => applyPreset(name)}
                  >
                    {name}
                  </Button>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </motion.section>

    <div className="mt-8 grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
      <motion.div
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.08 }}
      >
        <Card className="rounded-[2rem] border-white/10 bg-white/[0.04] backdrop-blur-xl">
          <CardHeader>
            <div className="flex items-center justify-between gap-4">
              <div>
                <SectionEyebrow>Scanner Dimensions</SectionEyebrow>
                <CardTitle className="text-3xl text-zinc-50">Structural Input Model</CardTitle>
                <CardDescription className="mt-2 max-w-2xl text-zinc-400">
                  Each dimension expresses one part of the ShovelsSale doctrine: durable
                  value lives where many participants depend on a layer regardless of who wins.
                </CardDescription>
              </div>
              <Layers3 className="h-8 w-8 text-amber-400" />
            </div>
          </CardHeader>
          <CardContent className="space-y-8">
            {DIMENSIONS.map((d) => (
              <div key={d.key} className="rounded-2xl border border-white/8 bg-black/20 p-5">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                  <div>
                    <div className="text-lg font-medium text-zinc-100">{d.label}</div>
                    <p className="mt-1 max-w-3xl text-sm leading-6 text-zinc-400">
                      {d.description}
                    </p>
                  </div>
                  <Badge className="rounded-full border border-amber-400/20 bg-amber-400/10 px-3 py-1 text-xs uppercase tracking-[0.18em] text-amber-300 hover:bg-amber-400/10">
                    {values[d.key]}/100
                  </Badge>
                </div>
                <div className="mt-5 px-1">
                  <Slider
                    value={[values[d.key]]}
                    min={0}
                    max={100}
                    step={1}
                    onValueChange={(v) => updateValue(d.key, v)}
                  />
                </div>
                <div className="mt-3 flex items-center justify-between text-xs uppercase tracking-[0.14em] text-zinc-500">
                  <span>{d.left}</span>
                  <span>{d.right}</span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.12 }}
        className="space-y-8"
      >
        <Card className="rounded-[2rem] border-white/10 bg-white/[0.04] backdrop-blur-xl">
          <CardHeader>
            <SectionEyebrow>Classification Output</SectionEyebrow>
            <CardTitle className="flex items-center gap-3 text-3xl text-zinc-50">
              <Landmark className="h-7 w-7 text-amber-400" />
              {assetName || "Unnamed Asset"}
            </CardTitle>
            <CardDescription className="text-zinc-400">{category}</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="rounded-3xl border border-amber-400/20 bg-amber-400/10 p-6">
              <div className="flex flex-wrap items-center gap-3">
                <Badge className="rounded-full border border-amber-400/30 bg-black/20 px-4 py-1.5 text-xs uppercase tracking-[0.22em] text-amber-300 hover:bg-black/20">
                  {scores.primary}
                </Badge>
                <Badge className="rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-xs uppercase tracking-[0.22em] text-zinc-200 hover:bg-white/5">
                  {scores.layer}
                </Badge>
                <Badge className="rounded-full border border-white/10 bg-white/5 px-4 py-1.5 text-xs uppercase tracking-[0.22em] text-zinc-200 hover:bg-white/5">
                  {scores.confidence} Confidence
                </Badge>
              </div>
              <h3 className="mt-5 text-2xl font-semibold text-zinc-50">
                {scores.narrative.headline}
              </h3>
              <p className="mt-4 text-base leading-8 text-zinc-300">{scores.narrative.body}</p>
              <div className="mt-5 flex flex-wrap gap-2">
                {scores.narrative.brief.map((item) => (
                  <Badge
                    key={item}
                    className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs tracking-[0.12em] text-zinc-300 hover:bg-white/5"
                  >
                    {item}
                  </Badge>
                ))}
              </div>
            </div>

            <div className="mt-6 grid gap-4 sm:grid-cols-2">
              <Card className="rounded-2xl border-white/10 bg-black/20">
                <CardHeader>
                  <CardTitle className="text-lg text-zinc-50">Top Signals</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {scores.strengths.map((s) => (
                    <div key={s.key}>
                      <div className="mb-2 flex items-center justify-between text-sm text-zinc-300">
                        <span>{s.label}</span>
                        <span>{s.value}</span>
                      </div>
                      <Progress value={s.value} className="h-2 bg-white/10" />
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card className="rounded-2xl border-white/10 bg-black/20">
                <CardHeader>
                  <CardTitle className="text-lg text-zinc-50">Weak Signals</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {scores.weaknesses.map((w) => (
                    <div key={w.key}>
                      <div className="mb-2 flex items-center justify-between text-sm text-zinc-300">
                        <span>{w.label}</span>
                        <span>{w.value}</span>
                      </div>
                      <Progress value={w.value} className="h-2 bg-white/10" />
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </CardContent>
        </Card>

        <Tabs defaultValue="radar" className="w-full">
          <TabsList className="grid w-full grid-cols-2 rounded-2xl border border-white/10 bg-white/5">
            <TabsTrigger value="radar" className="rounded-2xl">Structural Radar</TabsTrigger>
            <TabsTrigger value="class" className="rounded-2xl">Class Scores</TabsTrigger>
          </TabsList>
          <TabsContent value="radar">
            <Card className="rounded-[2rem] border-white/10 bg-white/[0.04] backdrop-blur-xl">
              <CardHeader>
                <CardTitle className="text-2xl text-zinc-50">Structural Profile</CardTitle>
                <CardDescription className="text-zinc-400">
                  Multi-dimensional shape of the asset under the ShovelsSale model.
                </CardDescription>
              </CardHeader>
              <CardContent className="h-[360px]">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="rgba(255,255,255,0.12)" />
                    <PolarAngleAxis dataKey="dimension" tick={{ fill: "#d4d4d8", fontSize: 12 }} />
                    <PolarRadiusAxis domain={[0, 100]} tick={false} axisLine={false} />
                    <Radar
                      name="Score"
                      dataKey="score"
                      stroke="#fbbf24"
                      fill="#fbbf24"
                      fillOpacity={0.28}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="class">
            <Card className="rounded-[2rem] border-white/10 bg-white/[0.04] backdrop-blur-xl">
              <CardHeader>
                <CardTitle className="text-2xl text-zinc-50">Class Distribution</CardTitle>
                <CardDescription className="text-zinc-400">
                  Relative weight of Extraction, Shovel, and Gatekeeper behaviors.
                </CardDescription>
              </CardHeader>
              <CardContent className="h-[360px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={classBars} margin={{ left: 0, right: 10, top: 10, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                    <XAxis dataKey="name" tick={{ fill: "#d4d4d8", fontSize: 12 }} />
                    <YAxis tick={{ fill: "#a1a1aa", fontSize: 12 }} domain={[0, 100]} />
                    <Tooltip cursor={{ fill: "rgba(255,255,255,0.03)" }} />
                    <Bar dataKey="score" fill="#fbbf24" radius={[10, 10, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </motion.div>
    </div>

    <motion.section
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.16 }}
      className="mt-8 grid gap-8 lg:grid-cols-[0.95fr_1.05fr]"
    >
      <Card className="rounded-[2rem] border-white/10 bg-white/[0.04] backdrop-blur-xl">
        <CardHeader>
          <SectionEyebrow>Reference Logic</SectionEyebrow>
          <CardTitle className="text-3xl text-zinc-50">The Structural Model</CardTitle>
          <CardDescription className="max-w-2xl text-zinc-400">
            This is the doctrinal core of the scanner. Every market can be reduced to three
            structural layers. The goal is not to participate blindly. The goal is to position
            where structural value compounds.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {[
            {
              icon: Sparkles,
              title: "Extraction Layer",
              body: "Where participants compete for visible outcomes. This is the noisiest layer, the most narratively attractive, and often the most fragile.",
            },
            {
              icon: Cpu,
              title: "Infrastructure Layer",
              body: "Where systems, tooling, logistics, compute, and utility enable the competition beneath the visible surface. This is where durable shovel value is built.",
            },
            {
              icon: ShieldCheck,
              title: "Control Layer",
              body: "Where standards, permissions, access, rails, and distribution rules are defined. This is where power outlasts narrative cycles.",
            },
          ].map((item) => {
            const Icon = item.icon;
            return (
              <div key={item.title} className="rounded-2xl border border-white/8 bg-black/20 p-5">
                <div className="flex items-center gap-3 text-zinc-50">
                  <Icon className="h-5 w-5 text-amber-400" />
                  <div className="text-lg font-medium">{item.title}</div>
                </div>
                <p className="mt-3 text-sm leading-7 text-zinc-400">{item.body}</p>
              </div>
            );
          })}
        </CardContent>
      </Card>

      <Card className="rounded-[2rem] border-white/10 bg-white/[0.04] backdrop-blur-xl">
        <CardHeader>
          <SectionEyebrow>Operational Doctrine</SectionEyebrow>
          <CardTitle className="text-3xl text-zinc-50">Decision Engine</CardTitle>
          <CardDescription className="text-zinc-400">
            ShovelsSale does not ask whether something is exciting. It asks whether it serves
            one participant, many participants, or the system itself.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-5">
          <div className="rounded-3xl border border-amber-400/20 bg-amber-400/10 p-6">
            <div className="text-xs uppercase tracking-[0.25em] text-amber-300">Core Question</div>
            <p className="mt-3 text-xl leading-9 text-zinc-100">
              Does this asset serve one participant — or all participants?
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-3">
            {[
              {
                title: "Miner",
                body: "Competes directly for the outcome. High narrative visibility. Higher outcome fragility.",
              },
              {
                title: "Shovel",
                body: "Enables many participants across the market. Utility compounds regardless of who wins.",
              },
              {
                title: "Gatekeeper",
                body: "Defines access, permissions, distribution, rails, or standards inside the market structure.",
              },
            ].map((item) => (
              <div key={item.title} className="rounded-2xl border border-white/8 bg-black/20 p-5">
                <div className="text-lg font-medium text-zinc-50">{item.title}</div>
                <p className="mt-3 text-sm leading-7 text-zinc-400">{item.body}</p>
              </div>
            ))}
          </div>

          <div className="rounded-2xl border border-white/8 bg-black/20 p-5">
            <div className="mb-3 flex items-center gap-2 text-zinc-50">
              <Scale className="h-5 w-5 text-amber-400" />
              <span className="text-lg font-medium">Interpretation Notes</span>
            </div>
            <p className="text-sm leading-7 text-zinc-400">
              A scanner like this does not replace analysis. It disciplines analysis. It turns
              aesthetic intuition into structural judgment and converts loose market language into
              a repeatable classification method.
            </p>
          </div>
        </CardContent>
      </Card>
    </motion.section>

    <motion.section
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.2 }}
      className="mt-8"
    >
      <Card className="rounded-[2rem] border-white/10 bg-white/[0.04] backdrop-blur-xl">
        <CardHeader>
          <SectionEyebrow>Strategic Use Cases</SectionEyebrow>
          <CardTitle className="text-3xl text-zinc-50">Why This Strengthens The Asset</CardTitle>
          <CardDescription className="max-w-3xl text-zinc-400">
            The Shovel Scanner does more than add interactivity. It converts ShovelsSale from a
            narrative property into intellectual infrastructure — a reference system that can be
            cited, reused, operationalized, and extended.
          </CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 lg:grid-cols-3">
          {[
            {
              icon: BookOpen,
              title: "Reference Authority",
              body: "It gives the site a native classification language. This moves ShovelsSale closer to a think-tank, research system, or market doctrine rather than a content site.",
            },
            {
              icon: Network,
              title: "Conceptual Moat",
              body: "A scanner built on your own framework reinforces the naming system: Miner, Shovel, Gatekeeper, Layer, Control. That language becomes proprietary mental territory.",
            },
            {
              icon: Binary,
              title: "Product Foundation",
              body: "This can evolve into a real product: public scanner, premium reports, industry maps, scoring database, or sovereign-grade market intelligence layer.",
            },
          ].map((item) => {
            const Icon = item.icon;
            return (
              <div key={item.title} className="rounded-2xl border border-white/8 bg-black/20 p-6">
                <Icon className="h-6 w-6 text-amber-400" />
                <div className="mt-4 text-xl font-medium text-zinc-50">{item.title}</div>
                <p className="mt-3 text-sm leading-7 text-zinc-400">{item.body}</p>
              </div>
            );
          })}
        </CardContent>
      </Card>
    </motion.section>

    <motion.section
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.24 }}
      className="mt-8 mb-10"
    >
      <Card className="overflow-hidden rounded-[2rem] border border-amber-400/20 bg-gradient-to-br from-amber-400/10 to-white/[0.03] backdrop-blur-xl">
        <CardContent className="flex flex-col gap-6 px-6 py-8 md:flex-row md:items-center md:justify-between md:px-8 md:py-10">
          <div className="max-w-3xl">
            <div className="text-xs uppercase tracking-[0.3em] text-amber-300">ShovelsSale Doctrine</div>
            <h2 className="mt-3 text-3xl font-semibold tracking-tight text-zinc-50 md:text-4xl">
              We do not chase hype. We classify the layers that make hype possible.
            </h2>
            <p className="mt-4 text-base leading-8 text-zinc-300">
              The Shovel Scanner is not a gimmick. It is the first operational instrument in a
              larger sovereign-grade system for analyzing how value is created, captured, and
              controlled in gold-rush markets.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Button className="rounded-full bg-amber-400 px-6 text-black hover:bg-amber-300">
              Open Full Framework <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button variant="outline" className="rounded-full border-white/10 bg-white/5 text-zinc-100 hover:bg-white/10">
              Read the Manifesto <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.section>
  </div>
</div>

); }
