TOOL.Category = "Test"
TOOL.Name = "Test Sphere"

-- PD 控制器参数（可在此处调整）
local Kp = 32.0 -- 比例增益
local Kd = 1.0  -- 微分增益（增大可减少过冲和振荡）

function TOOL:LeftClick(tr)
    local clickPos = tr.HitPos
    if not IsValid(self.sphere) then
        self.sphere = ents.Create("prop_sphere")
        self.sphere:SetKeyValue("radius", 23)
        self.sphere:SetPos(clickPos + Vector(0, 0, 24))
        self.sphere:SetModel("models/hunter/misc/sphere1x1.mdl")
        self.sphere:Spawn()

        local physObj = self.sphere:GetPhysicsObject()

        physObj:SetMass(1)
        physObj:SetInertia(Vector(1, 1, 1))
        physObj:EnableDrag(false)

        local _, angular = physObj:GetDamping()
        physObj:SetDamping(0, angular) -- 不使用内置阻尼，由 PD 控制完全接管

        physObj:Wake()
    else
        self.sphere:Remove()
    end
end

function TOOL:RightClick(tr)
    self.targetPos = tr.HitPos
end

function TOOL:Reload(tr)
    PrintTable(self.sphere:GetPhysicsObject():GetFrictionSnapshot())
end

function TOOL:Think()
    if not IsValid(self.sphere) then return end
    if not self.targetPos then return end

    local phys = self.sphere:GetPhysicsObject()
    if not IsValid(phys) then return end

    local currentPos = self.sphere:GetPos()
    local velocity = phys:GetVelocity()
    local target = self.targetPos

    -- 水平误差
    local errorX = target.x - currentPos.x
    local errorY = target.y - currentPos.y

    -- PD 控制力计算：F = Kp * error - Kd * velocity
    local forceX = Kp * errorX - Kd * velocity.x
    local forceY = Kp * errorY - Kd * velocity.y
    local force = Vector(forceX, forceY, 0)

    -- 限制最大力（防止数值爆炸）
    local maxForce = 1200
    if force:Length() > maxForce then
        force = force:GetNormalized() * maxForce
    end

    phys:ApplyForceCenter(force)

    -- 数据打印（保持不变）
    print(string.format("%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f",
        CurTime(),
        currentPos.x, currentPos.y,
        velocity.x, velocity.y,
        errorX, errorY,
        target.x, target.y
    ))
end
